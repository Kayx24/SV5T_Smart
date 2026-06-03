import pytest
from normalizer import UniversalNormalizer, safe_float, safe_bool, safe_int

# ==========================================
# 1. TEST CÁC HÀM ÉP KIỂU (HELPER FUNCTIONS)
# ==========================================

def test_safe_float():
    """Kiểm tra xử lý số thực (điểm số)."""
    assert safe_float("8.5") == 8.5
    assert safe_float("8,5") == 8.5         # Lỗi dấu phẩy kinh điển của VN
    assert safe_float(" 9,2 ") == 9.2       # Có khoảng trắng thừa
    assert safe_float("Thiếu điểm") == 0.0  # Chữ nhập bậy vào cột số
    assert safe_float(None) == 0.0          # Ô bị bỏ trống

def test_safe_bool():
    """Kiểm tra bẫy True/False nguy hiểm nhất."""
    assert safe_bool(True) is True
    assert safe_bool("Có") is True
    assert safe_bool("Đạt") is True
    
    # Các trường hợp phải ra False
    assert safe_bool("Không có") is False
    assert safe_bool("False") is False
    assert safe_bool("0") is False
    assert safe_bool(None) is False
    assert safe_bool("") is False

def test_safe_int():
    """Kiểm tra xử lý số nguyên (số ngày tình nguyện)."""
    assert safe_int("15") == 15
    assert safe_int("15.0") == 15      # File Excel hay tự biến int thành float
    assert safe_int("Mười lăm") == 0   # Lỗi nhập tay

# ==========================================
# 2. TEST LOGIC ÁNH XẠ (MAPPING & NORMALIZING)
# ==========================================

@pytest.fixture
def normalizer():
    """Khởi tạo Normalizer dùng chung cho các test case."""
    return UniversalNormalizer(mapping_path='mapping.json')

def test_mapping_messy_headers(normalizer):
    """Kiểm tra xem hệ thống có nhận diện đúng cột dù tên lộn xộn không."""
    raw_row = {
        "   Mã Số SV ": 20520000,
        "ĐIỂM TB": "8,5",
        "Số Ngày Tình Nguyện": 15
    }
    
    mapped = normalizer._map_row_keys(raw_row)
    
    # Kì vọng hệ thống phải gom về đúng key chuẩn
    assert mapped["student_id"] == 20520000
    assert mapped["gpa"] == "8,5"
    assert mapped["volunteer_days"] == 15
    # Cột không có trong raw_row thì giá trị map phải là None
    assert mapped["ielts"] is None 

def test_full_row_normalization(normalizer):
    """Kiểm tra toàn bộ luồng làm sạch 1 dòng dữ liệu sinh viên."""
    raw_row = {
        "mssv": 20520123.0,                  # Bị float hóa
        "họ và tên": "   Nguyễn Văn A   ",   # Khoảng trắng thừa
        "trung bình tích lũy": "8,75",       # Dấu phẩy
        "điểm rèn luyện": "Chín mươi",       # Nhập chữ thay vì số
        "kỹ năng mềm": "Không có chứng nhận",# String có nghĩa là False
        "giải thưởng học thuật": "Giải Nhất" # String có nghĩa là True
    }
    
    # Bước 1: Map headers
    mapped = normalizer._map_row_keys(raw_row)
    # Bước 2: Normalize values
    clean_data = normalizer.normalize_student_data(mapped)
    
    # Kiểm tra kết quả cuối cùng
    assert clean_data["student_id"] == "20520123" # Đã mất đuôi .0 và thành chuỗi
    assert clean_data["student_name"] == "Nguyễn Văn A" # Đã xóa khoảng trắng
    assert clean_data["gpa"] == 8.75              # Thành float chuẩn
    assert clean_data["conduct_score"] == 0.0     # Không parse được chữ -> 0.0
    assert clean_data["soft_skill_certificate"] is False # Hiểu được ý nghĩa "Không"
    assert clean_data["academic_award"] is True   # Có chữ là có giải (True)