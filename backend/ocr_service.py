from abc import ABC, abstractmethod
import os

# ==========================================
# TASK 6: THIẾT KẾ INTERFACE CHUẨN
# ==========================================
class BaseOCR(ABC):
    """
    Khuôn mẫu chuẩn cho mọi công cụ đọc ảnh sau này.
    Bất kỳ class OCR nào được tạo ra cũng BẮT BUỘC phải có hàm extract_text.
    """
    @abstractmethod
    def extract_text(self, image_path: str) -> str:
        """Hàm này sẽ nhận đường dẫn ảnh và trả về chuỗi văn bản."""
        pass

# ==========================================
# TASK 5: CHUẨN BỊ OCR PLACEHOLDER
# ==========================================
class MockOCR(BaseOCR):
    """
    Công cụ đọc ảnh giả lập dùng để test luồng (Pipeline) và Rules Engine 
    trước khi ghép model AI thật vào.
    """
    def __init__(self):
        # Bộ từ điển giả lập: Tên file ảnh -> Nội dung text mô phỏng trả về
        self.mock_database = {
            "the_luc_tot.jpg": "Chứng nhận Thanh niên khỏe cấp Trường năm 2023",
            "giai_nhat_nckh.png": "Quyết định khen thưởng Giải Nhất Nghiên cứu khoa học sinh viên",
            "mua_he_xanh.jpg": "Giấy chứng nhận tham gia chiến dịch Mùa hè xanh",
            "khong_hop_le.jpg": "Biên lai đóng học phí kỳ 1"
        }

    def extract_text(self, image_path: str) -> str:
        """Giả lập việc trích xuất văn bản từ ảnh."""
        print(f"[MockOCR] Đang phân tích ảnh minh chứng: {image_path} ...")
        
        # Chỉ lấy tên file (ví dụ: the_luc_tot.jpg) từ đường dẫn dài
        filename = os.path.basename(image_path)
        
        # Nếu tên file có trong từ điển giả lập thì trả về text đó, 
        # Nếu ảnh lạ thì báo không đọc được.
        return self.mock_database.get(filename, "Không trích xuất được thông tin hoặc ảnh không hợp lệ")

# ==========================================
# TEST CHẠY THỬ NHANH
# ==========================================
if __name__ == "__main__":
    ocr = MockOCR()
    
    print("--- TEST MOCK OCR ---")
    # Test một ảnh hợp lệ (giả sử đường dẫn người dùng upload lên như vầy)
    text1 = ocr.extract_text("C:/uploads/the_luc_tot.jpg")
    print(f"Kết quả 1: {text1}\n")
    
    # Test một ảnh lạ không có trong database giả lập
    text2 = ocr.extract_text("C:/uploads/anh_tu_suong_cua_sinh_vien.png")
    print(f"Kết quả 2: {text2}")