# 🖥️ SV5T Smart - Frontend Dashboard (`app.py`)

> Tệp `app.py` là trung tâm điều khiển giao diện người dùng (UI) của hệ thống **SV5T AI Reviewer Platform**, được xây dựng trên nền tảng **Streamlit**. Tệp này đóng vai trò là cầu nối tương tác giữa cán bộ xét duyệt và các luồng xử lý lõi (AI, Rule Engine) ở backend.

---

## 🎯 Nhiệm vụ chính

1. **Giao diện điều hành trực quan (Dashboard):** Cung cấp góc nhìn tổng quan theo thời gian thực về tiến độ xét duyệt hồ sơ Sinh viên 5 tốt.
2. **Điểm chạm dữ liệu (Data Ingestion):** Cho phép người dùng tải lên danh sách sinh viên (Batch Upload) để kích hoạt quá trình tự động đánh giá.
3. **Trình diễn kết quả (Data Visualization):** Vẽ biểu đồ và bảng biểu động dựa trên dữ liệu lấy từ cơ sở dữ liệu SQLite (`sv5tot.db`).

---

## 🧩 Cấu trúc giao diện (Layout)

Giao diện được thiết kế theo dạng **Wide Layout**, chia làm 2 thành phần chính:

### 1. Khu vực Sidebar (Điều hướng bên trái)
- **Tiêu đề & Thông tin:** Nhận diện hệ thống và user profile (hiện tại là Admin).
- **Demo Generator:** Nút công cụ hỗ trợ cho việc Kiểm thử (Testing). Khi bấm nút, hệ thống sẽ tự động tạo ra một sinh viên ảo và đưa vào luồng chấm điểm. Tỷ lệ được cấu hình là cứ tạo 4 sinh viên trượt (FAIL) thì sẽ tạo 1 sinh viên đậu (PASS) để làm phong phú dữ liệu biểu đồ.
- **Menu điều hướng:** Điều hướng giữa các chức năng (hiện tại tập trung vào trang "Tổng quan").

### 2. Khu vực Main Content (Nội dung chính)
Được thiết kế theo nguyên tắc thẻ (Cards) bo viền hiện đại, tương thích tốt với cả hệ màu Sáng (Light Mode) và Tối (Dark Mode).

- **Khu vực Tải lên hồ sơ (Batch Upload):** 
  - Hỗ trợ kéo thả các file `Excel`, `CSV` (hoặc ảnh/PDF trong tương lai). 
  - Kích hoạt hàm `process_batch()` từ backend và hiển thị hiệu ứng thành công (`st.balloons()`) sau khi hoàn tất.
  
- **Chỉ số KPI (Key Performance Indicators):** 
  - Sử dụng HTML/CSS nội tuyến để tạo các thẻ Gradient nổi bật.
  - Thống kê tự động các thông số: **Tổng hồ sơ**, số lượng **Đã duyệt (PASS)** và **Bị từ chối (FAIL)**.
  
- **Biểu đồ (Data Visualization):** 
  - Sử dụng thư viện `plotly.express` dạng Donut Charts (Pie chart với `hole=0.6`).
  - **Tổng quan đánh giá:** Tỷ lệ hồ sơ Đạt / Không đạt.
  - **Risk Level:** Tỷ lệ rủi ro của các hồ sơ (Cao / Trung bình / Thấp) giúp cán bộ đánh giá chất lượng hồ sơ của đợt nộp.

- **Bảng "Hoạt động gần đây" (Recent Activity):**
  - Bảng HTML tùy chỉnh với CSS badges.
  - Liệt kê 10 hồ sơ được xử lý gần nhất bao gồm: Thời gian, Mã hồ sơ, Tên sinh viên, Tiêu chí chưa đạt (bóc tách thành danh sách `•` trực quan từ Rule Engine), và Trạng thái (PASS/FAIL).

---

## ⚙️ Luồng kết nối với Backend

Tệp `app.py` không tự thực hiện logic chấm điểm mà sẽ gọi trực tiếp đến thư mục `backend/`:

1. **Kết nối DB:** Thiết lập đường dẫn tuyệt đối đến tệp `backend/sv5tot.db` và sử dụng `pandas.read_sql()` để truy vấn toàn bộ bảng `student_evaluations` mỗi khi trang được tải lại (`st.rerun()`).
2. **Import xử lý lõi:**
   ```python
   from main import process_student
   from batch_processor import process_batch
   ```
   Khi có dữ liệu nạp vào (từ nút Demo hoặc tải file Batch), `app.py` sẽ đẩy dữ liệu sang các hàm này để backend thực thi Rule Engine & lưu xuống DB.

---

## 🚀 Hướng dẫn chạy giao diện

Bạn phải luôn chạy file này từ thư mục gốc của toàn bộ dự án để các đường dẫn tới Backend hoạt động chính xác.

Mở terminal (tại thư mục `D:\GitHub\SV5T_Smart\`) và gõ lệnh:

```bash
streamlit run frontend/app.py
```

Trình duyệt sẽ tự động mở tại địa chỉ `http://localhost:8501`.

---

## 🎨 Tùy biến CSS
Các cấu phần giao diện (đặc biệt là bảng hoạt động gần đây) sử dụng các biến CSS mặc định của Streamlit (ví dụ: `var(--background-color)`, `var(--text-color)`, `var(--secondary-background-color)`) để tự động thích ứng mượt mà khi người dùng chuyển đổi Theme Sáng / Tối trên trình duyệt.