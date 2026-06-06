import json
import pandas as pd
import re
import os

# ==========================================
# HELPER FUNCTIONS: Ép kiểu an toàn (Safe Casting)
# ==========================================

def safe_str(val, default="UNKNOWN"):
    """Ép kiểu chuỗi an toàn, loại bỏ khoảng trắng thừa."""
    if pd.isna(val) or val is None or str(val).strip() == "":
        return default
    return str(val).strip()

def safe_float(val, default=0.0):
    """Ép kiểu số thực (float), xử lý dấu phẩy thập phân của VN."""
    if pd.isna(val) or val is None:
        return default
    try:
        # Xóa khoảng trắng và đổi phẩy thành chấm (VD: "8,5" -> "8.5")
        cleaned_val = str(val).replace(',', '.').strip()
        # Loại bỏ các ký tự không phải số hoặc dấu chấm
        cleaned_val = re.sub(r'[^\d.]', '', cleaned_val)
        return float(cleaned_val) if cleaned_val else default
    except ValueError:
        return default

def safe_int(val, default=0):
    """Ép kiểu số nguyên (int)."""
    if pd.isna(val) or val is None:
        return default
    try:
        # Tránh trường hợp float string như "10.0" -> int
        return int(float(str(val).replace(',', '.').strip()))
    except (ValueError, TypeError):
        return default

def safe_bool(val, default=False):
    """
    Ép kiểu boolean an toàn dựa trên ngữ nghĩa.
    Giải quyết triệt để bẫy bool("Không có") -> True của Python.
    """
    if pd.isna(val) or val is None:
        return default
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return val > 0
    
    text = str(val).lower().strip()
    if text == "":
        return False
    # Danh sách các từ khóa mang ý nghĩa "Không / False"
    negative_prefixes = ["0", "false", "không", "ko", "chưa", "none", "không có", "null"]
    for neg in negative_prefixes:
        if text.startswith(neg):
            return False
    return True

# ==========================================
# MAIN CLASS: Normalizer
# ==========================================

class UniversalNormalizer:
    def __init__(self, mapping_path: str = 'mapping.json'):
        """Khởi tạo Normalizer, load từ điển mapping."""
        self.mapping = {}
        # Hỗ trợ lấy đường dẫn tuyệt đối để tránh lỗi khi gọi từ main.py
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_mapping_path = os.path.join(base_dir, mapping_path)
        
        try:
            with open(full_mapping_path, 'r', encoding='utf-8') as f:
                self.mapping = json.load(f)
        except FileNotFoundError:
            print(f"[CẢNH BÁO] Không tìm thấy {full_mapping_path}. Hệ thống sẽ dùng key gốc.")

    def _clean_header(self, text: str) -> str:
        """Làm sạch tên cột để dễ mapping (xóa khoảng trắng, in thường)."""
        return re.sub(r'\s+', ' ', str(text)).strip().lower()

    def _map_row_keys(self, raw_row: dict) -> dict:
        """
        Nhận vào 1 dòng dữ liệu thô (dict), dùng mapping.json 
        để chuyển các key lộn xộn thành key chuẩn của hệ thống.
        """
        mapped_data = {}
        
        # Làm sạch các key của dữ liệu thô hiện tại
        clean_raw_keys = {k: self._clean_header(k) for k in raw_row.keys()}
        
        for standard_key, aliases in self.mapping.items():
            mapped_data[standard_key] = None # Mặc định là None nếu không tìm thấy
            
            for original_key, clean_key in clean_raw_keys.items():
                if clean_key in [self._clean_header(a) for a in aliases]:
                    mapped_data[standard_key] = raw_row[original_key]
                    break # Tìm thấy cột tương ứng thì dừng tìm cho key chuẩn này
                    
        return mapped_data

    def normalize_student_data(self, mapped_data: dict) -> dict:
        """
        Thực hiện ép kiểu dữ liệu dựa trên key chuẩn đã được map.
        Đây là phiên bản an toàn từ logic cũ của ông.
        """
        normalized = {}

        # ==========================================
        # BASIC INFO
        # ==========================================
        # Nếu mã số sinh viên là số (VD: 20520000.0), safe_str sẽ ra "20520000.0". 
        # Cần biến về int trước nếu nó dạng số để loại bỏ đuôi .0
        raw_id = mapped_data.get("student_id")
        if isinstance(raw_id, float) and pd.notna(raw_id):
            raw_id = str(int(raw_id))
            
        normalized["student_id"] = safe_str(raw_id, default="UNKNOWN")
        normalized["student_name"] = safe_str(mapped_data.get("student_name"), default="UNKNOWN")
        normalized["university"] = safe_str(mapped_data.get("university"), default="UNKNOWN")

        # ==========================================
        # SCORES
        # ==========================================
        normalized["gpa"] = safe_float(mapped_data.get("gpa"))
        normalized["conduct_score"] = safe_float(mapped_data.get("conduct_score"))
        normalized["ielts"] = safe_float(mapped_data.get("ielts"))
        normalized["volunteer_days"] = safe_int(mapped_data.get("volunteer_days"))

        # ==========================================
        # ACADEMIC, PHYSICAL, VOLUNTEER, INTEGRATION, DISCIPLINE
        # ==========================================
        # Dùng vòng lặp cho các cột boolean để code gọn và dễ bảo trì
        bool_fields = [
           "research", "academic_award", "publication", "physical_certificate", 
            "sports_award", "volunteer_award", "soft_skill_certificate", 
            "international_activity", "integration_award", "disciplinary_action"
        ]
        
        for field in bool_fields:
            normalized[field] = safe_bool(mapped_data.get(field))

        return normalized

    def process_file(self, file_path: str) -> list[dict]:
        """
        Pipeline xử lý toàn bộ: Đọc file Excel/CSV -> Map Headers -> Normalize Từng Dòng.
        Trả về list các dict chuẩn xác để nhét vào Database hoặc Rules Engine.
        """
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
        except Exception as e:
            print(f"[LỖI] Không thể đọc file {file_path}: {e}")
            return []

        # Xóa các dòng rỗng hoàn toàn
        df.dropna(how='all', inplace=True)
        
        # Chuyển DataFrame thành list of dicts (mỗi dict là 1 dòng)
        raw_records = df.to_dict(orient='records')
        
        clean_records = []
        for row in raw_records:
            # 1. Map key lộn xộn -> key chuẩn
            mapped_row = self._map_row_keys(row)
            # 2. Ép kiểu và chuẩn hóa giá trị
            clean_row = self.normalize_student_data(mapped_row)
            clean_records.append(clean_row)
            
        return clean_records

# ==========================================
# CHẠY THỬ NGHIỆM (Demo)
# ==========================================
if __name__ == "__main__":
    # Khởi tạo
    normalizer = UniversalNormalizer(mapping_path='mapping.json')
    
    # Dữ liệu rác giả lập (Tên cột lộn xộn, dữ liệu chứa string/float lẫn lộn)
    mock_df = pd.DataFrame({
        "  Mã SV ": [20520001, None],
        "Họ Tên  ": ["Nguyễn Văn A", "Trần Thị B"],
        "GPA": ["8,5", "Thiếu điểm"],       # 8,5 -> 8.5 | "Thiếu điểm" -> 0.0
        "ĐRL": [85.5, 90],                   # 85.5 -> 85.5 | 90 -> 90.0
        "Số ngày tình nguyện": [15, "10"],   # 15 -> 15 | "10" -> 10
        "Giải thưởng Học thuật": ["Có", "Không có"],  # "Có" -> True | "Không có" -> False
        "Kỷ luật": ["Không", "Có vi phạm"]            # "Không" -> False | "Có vi phạm" -> True
    })
    
    mock_df.to_excel("temp_test.xlsx", index=False)
    
    # Chạy pipeline
    results = normalizer.process_file("temp_test.xlsx")
    
    print("KẾT QUẢ CHUẨN HÓA:")
    print(json.dumps(results, indent=2, ensure_ascii=False))