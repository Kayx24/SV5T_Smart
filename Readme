# 🎓 SMARTV5T - AI-POWERED STUDENT EVALUATION & REVIEW SYSTEM

> Hệ thống trợ lý trí tuệ nhân tạo phối hợp bộ lọc quy chế (Rule Engine) hỗ trợ tự động hóa, thẩm định diện rộng và quản lý hàng đợi xét chọn danh hiệu **Sinh viên 5 tốt cấp Trung ương**.

---

## 1. 🎯 Giới thiệu đề tài & Mục tiêu hệ thống

**SmartV5T** là giải pháp công nghệ toàn diện được thiết kế chuyên biệt để giải quyết bài toán thắt cổ chai hành chính trong mỗi mùa xét duyệt hồ sơ danh hiệu Sinh viên 5 tốt tại các cơ sở giáo dục đại học. Hệ thống là sự kết hợp chặt chẽ giữa bộ lọc quy tắc cứng (Rule Engine) và Trí tuệ nhân tạo (Explainable AI).

### ⚖️ Triết lý vận hành cốt lõi: AI-Assisted, Not Decision-Maker
* Hệ thống **KHÔNG** thay thế con người hay Hội đồng ban giám khảo.
* Quyết định `PASS/FAIL` được phân loại độc lập và minh bạch bởi **Rule Engine** dựa trên văn bản quy chế chính thức.
* **Trợ lý AI Agent** đóng vai trò đồng hành: tự động đọc hiểu, tổng hợp thế mạnh, phân tích rủi ro và tự động viết biên bản giải trình (Reasoning) nhằm hỗ trợ tối đa cho cán bộ kiểm định.

---

## 2. 🔀 Sơ đồ luồng xử lý hệ thống (Data Pipeline Workflow)

Dòng chảy dữ liệu trong hệ thống được module hóa khép kín nhằm bảo đảm hiệu năng xử lý song song:

```text
  [Nạp tài liệu thô] (Excel / CSV / Sắp tới là PDF/Ảnh minh chứng)
          │
          ▼
  [Lớp chuẩn hóa & Sửa lỗi] (Column Normalizer & Format Auto-Recovery)
          │
          ▼
  [Bộ lọc quy chế cứng] (Deterministic Rule Engine) ──► Tính toán Risk & Confidence Score
          │                                                    │
          ▼ (Phân loại PASS / FAIL)                            ▼ (Đính kèm chỉ số rủi ro)
  [Tầng dữ liệu vật lý] (SQLite Database via SQLAlchemy ORM) ◄─┘
          │
          ▼
  [Hàng đợi điều phối tập trung] (Queue Management UI)
          │
          ▼ (On-Demand Trigger / Cán bộ click xem hồ sơ cụ thể)
  [AI Analytics Agent] (Gemini 2.5 Flash / Trí tuệ nhân tạo)
          │
          ▼
  [Trạm thanh tra chuyên sâu] (Reviewer Dashboard Panel)
```

---

## 3. 🛠️ Hệ sinh thái công nghệ sử dụng (Tech Stack)

Hệ thống ưu tiên sử dụng các thư viện mã nguồn mở mạnh mẽ, đảm bảo tính gọn nhẹ, bảo mật và tốc độ thực thi tối ưu:

* **💻 Giao diện điều hành (Frontend):** **Streamlit** (Hỗ trợ xây dựng giao diện Dashboard tương tác trực quan thời gian thực).
* **⚙️ Bộ xử lý trung tâm (Backend Core):** **Python 3.11+** (Xử lý tác vụ, bóc tách cấu trúc tệp).
* **🗄️ Tầng lưu trữ (Database Layer):** **SQLite** phối hợp thư viện trừu tượng hóa **SQLAlchemy ORM** quản lý thực thể.
* **🧠 Trí tuệ nhân tạo (Core AI Model):** **Gemini 2.5 Flash API** (Đảm nhiệm vai trò viết biên bản lập luận văn bản tự nhiên).
* **📊 Xử lý & Trực quan dữ liệu (Data Crunching):** **Pandas** (Làm sạch tệp bảng tính).

---

## 4. 📝 Bộ tiêu chuẩn quy chế cứng (Rule-Based Engine Rules)

Hệ thống đối sánh dữ liệu đầu vào dựa trên các thông số sàn được cấu hình độc lập tại tệp `config_rules.json`:

### 🏅 5 Tiêu chí cốt lõi xét chọn danh hiệu Trung ương
1.  **⭐ Đạo đức tốt:** Điểm rèn luyện (`conduct_score`) bắt buộc phải đạt từ **90/100** điểm trở lên VÀ không có hành vi vi phạm kỷ luật (`disciplinary_action` phải là `False`).
2.  **📚 Học tập tốt:** Điểm trung bình học tập (`gpa`) đạt từ **3.6/4.0** trở lên (Hệ tín chỉ) VÀ bắt buộc phải có hoạt động bổ trợ học thuật như: Tham gia nghiên cứu khoa học (`research`), Đạt giải thưởng học thuật (`academic_award`), hoặc có Bài báo chuyên ngành (`publication`).
3.  **💪 Thể lực tốt:** Phải đạt chứng nhận "Sinh viên khỏe" (`physical_certificate` là `True`) hoặc Đạt giải thưởng thi đấu thể thao phong trào (`sports_award` là `True`).
4.  **🤝 Tình nguyện tốt:** Tích lũy thời gian hoạt động xã hội tối thiểu **5 ngày tình nguyện/năm** (`volunteer_days >= 5`) hoặc được trao tặng Giấy khen tình nguyện (`volunteer_award` là `True`).
5.  **🌐 Hội nhập tốt:** Đạt trình độ ngoại ngữ tương đương **IELTS >= 6.0** VÀ sở hữu ít nhất một chứng nhận bổ trợ (Chứng chỉ kỹ năng mềm `soft_skill_certificate`, Hoạt động quốc tế `international_activity`, hoặc Giải thưởng hội nhập `integration_award`).

---

## 5. 📂 Sơ đồ cấu trúc thư mục & Tài liệu tệp mã nguồn

Không gian làm việc được tổ chức phân lớp nghiêm ngặt, chia tách rõ ràng trách nhiệm giữa Tầng dữ liệu, Tầng xử lý logic và Tầng giao diện UI:

```text
D:\HOCTAP\SV5T-2\
├── backend/                             # Tầng xử lý Logic và Cơ sở dữ liệu
│   ├── config_rules.json                # File cấu hình các mốc điểm quy chế sàn cứng
│   ├── database.py                      # Thiết lập Session, hàm kết nối SQLite vĩnh viễn
│   ├── init_db.py                       # Tập lệnh khởi tạo bảng vật lý trong CSDL SQLite
│   ├── main.py                          # Trung tâm điều phối Pipeline, phân tích Risk/Confidence
│   ├── models.py                        # Khai báo Schema ánh xạ cơ sở dữ liệu SQLAlchemy
│   ├── normalizer.py                    # Khối định dạng và chuẩn hóa cấu trúc dữ liệu API
│   ├── reasoning.py                     # Cấu hình Prompt Engineering kết nối tới Google Generative AI
│   └── rules_engine.py                  # Module thực thi thuật toán kiểm tra logic PASS/FAIL
├── frontend/                            # Tầng giao diện tương tác người dùng
│   └── app.py                           # Dashboard giao diện điều hành Split-Panel (Queue + Inspector)
├── dataset/                             # Thư mục lưu trữ bộ dữ liệu thử nghiệm
│   ├── [SmartV5T] Unlabeled Dataset.xlsx # Tập dữ liệu thô phục vụ kiểm thử Batch Review
│   └── mock_documents/                  # Bản phác thảo hồ sơ tài liệu thành phần
├── .env                                 # Lưu trữ các biến môi trường và API Keys bí mật
└── requirements.txt                     # Danh sách các thư viện phụ thuộc của hệ thống
```

### 🗃️ Chi tiết chức năng từng File mã nguồn Backend

* **`models.py` (Cấu trúc bảng thực thể):** Định nghĩa bảng CSDL `student_evaluations`. Lưu trữ tất cả các trường dữ liệu tĩnh của sinh viên kết hợp với các cột nâng cao phục vụ điều phối như: `batch_id` (Phân loại đợt nộp), `risk_level` (Mức độ rủi ro), `confidence_score` (Độ tự tin thuật toán), và `reviewer_decision/notes` (Quyết định của con người).
* **`database.py` (Quản lý kết nối):** Quản lý vòng đời mở/đóng kết nối phiên làm việc với cơ sở dữ liệu. Tích hợp cơ chế xác định đường dẫn tuyệt đối (`Absolute Path`) thông qua thư viện `os.path`. Giải pháp Senior này giúp file dữ liệu `sv5tot.db` luôn cố định tại một vị trí duy nhất trong thư mục `backend`, loại bỏ hoàn toàn lỗi nhân bản hoặc mất dấu file DB khi khởi chạy app từ các terminal khác nhau.
* **`init_db.py` (Khởi tạo hệ thống):** Gọi lệnh tạo bảng vật lý tự động `Base.metadata.create_all(bind=engine)`. Được chạy một lần duy nhất khi hệ thống nâng cấp hoặc thay đổi cấu trúc cột trong mô hình dữ liệu.
* **`rules_engine.py` (Cơ chế quy tắc phân loại):** Đọc file cấu hình `config_rules.json`, chạy các câu lệnh so sánh toán học để bóc tách lý do loại (`reasons`) đối với các hồ sơ không đạt điều kiện sàn. Trả về cấu trúc JSON minh bạch phục vụ tính năng giải trình.
* **`reasoning.py` (Bộ não AI lập luận):** Thiết lập kết nối bảo mật đến mô hình `gemini-2.5-flash`. Sử dụng kỹ thuật Role-Prompting đóng vai Hội đồng kiểm định cấp Trung ương để bóc tách điểm mạnh, điểm yếu, phân tích rủi ro và đưa ra khuyến nghị hành động cho cán bộ duyệt.
* **`main.py` (Trạm điều phối lõi):** Chứa hàm chính `process_student()`. Hàm này chịu trách nhiệm nhận dữ liệu, gọi bộ rà soát quy chế, gán cờ tính toán các chỉ số rủi ro, chỉ số gian lận, quyết định việc gọi AI ngay lập tức hay trì hoãn, và lưu trữ bản ghi hoàn chỉnh xuống CSDL SQLite.

---

## 6. 🚀 Sáng kiến kỹ thuật & Tính năng vượt trội cấp cao (Senior Concepts)

Hệ thống sở hữu 3 giải thuật quan trọng giúp tối ưu hóa hiệu năng, giải quyết triệt để các bài toán thực tế của hệ thống doanh nghiệp lớn:

### ⚡ 1. Cơ chế "Chấm lười" (Lazy AI Evaluation) - Triệt tiêu lỗi Rate Limit 429
> **Bài toán thực tế:** Khi cán bộ sử dụng tính năng **Batch Review** tải lên tệp Excel chứa hàng trăm sinh viên cùng lúc, việc gọi API LLM liên tục trong vòng vài giây sẽ kích hoạt hệ thống phòng vệ của Google, gây lỗi nghẽn IP và sập luồng xử lý do vượt quá hạn mức (`Quota Exceeded 429`).
* **Sáng kiến kỹ thuật:** Hệ thống tích hợp tham số `skip_ai=True` khi thực thi xử lý hàng loạt. Trong quá trình quét vòng lặp qua file Excel, hệ thống chỉ chạy bộ lọc quy chế cứng bằng thuật toán cục bộ chạy bằng CPU (Tốc độ ánh sáng, mất chưa tới 1 giây cho 100 dòng) và ghi xuống DB một đoạn biên bản tạm thời.
* **Cơ chế On-Demand Trigger:** Chỉ khi cán bộ kiểm định nhấp chuột lựa chọn đích danh một sinh viên cụ thể trong hàng đợi (Queue Layout) ở cột trái giao diện web, hệ thống mới lập tức kích hoạt luồng mạng gọi API Gemini riêng biệt cho sinh viên đó để nâng cấp thành Biên bản lập luận chuyên sâu. Giải pháp này giúp hệ thống đạt tốc độ xử lý tức thì, tiết kiệm 95% tài nguyên token và xóa bỏ hoàn toàn lỗi sập luồng 429.

### 🛠️ 2. Thuật toán Regex tự phục hồi dữ liệu lỗi định dạng Excel
* **Bài toán thực tế:** Một lỗi định dạng cực kỳ phổ biến của Microsoft Excel là tự động chuyển đổi các ô điểm số học tập (Ví dụ: `3.9`) thành một chuỗi ngày tháng năm (`2026-09-03`) do lỗi múi giờ của hệ thống. Nếu ném trực tiếp vào Rule Engine, phần mềm sẽ crash lập tức vì không thể so sánh toán học giữa định dạng ngày tháng và số thực.
* **Giải pháp:** Giao diện tích hợp hàm xử lý thông minh `parse_excel_gpa()`. Khi phát hiện dữ liệu cell có định dạng ngày (`datetime.date`), thuật toán sử dụng Biểu thức chính quy (`Regex`) để bóc tách giá trị ngày/tháng, tự động tính toán quy đổi ngược trở về đúng con số thập phân chuẩn xác `3.9` ban đầu mà không cần con người can thiệp chỉnh sửa thủ công.

### 🚨 3. Hệ thống phân tích Chỉ số thông minh & Gắn cờ gian lận (Fraud Detection)
Mỗi bản ghi được đẩy qua Pipeline trung tâm đều được hệ thống chấm điểm và dán nhãn các chỉ số quản trị bao gồm:
* **Mức độ rủi ro (Risk Level):** 
    * `HIGH 🔴:` Hồ sơ không vượt qua các mốc điều kiện cứng (Loại thẳng khỏi hàng đợi).
    * `MEDIUM 🟡:` Hồ sơ đạt điều kiện, nhưng có các thông số nằm sát nút ranh giới sàn quy chế (Ví dụ: GPA từ 3.60 đến 3.65 hoặc giờ tình nguyện vừa khít mức tối thiểu). Hệ thống đổi màu cảnh báo màu vàng để cán bộ lưu ý mở tài liệu minh chứng ra hậu kiểm kỹ bằng tay.
    * `LOW 🟢:` Hồ sơ đạt các thông số cách biệt an toàn so với mức sàn quy chế.
* **Gắn cờ nghi vấn gian lận (Suspicious Flags):** Thuật toán tự động quét dữ liệu và gắn cờ cảnh báo rủi ro nếu phát hiện thông số vượt quá logic thực tế (Ví dụ: Ứng viên khai điểm GPA hệ 4 vượt ngưỡng `4.0` hoặc số giờ tham gia hoạt động tình nguyện quy đổi vượt mức `300` ngày thực tế), giúp hỗ trợ đắc lực cho công tác hậu kiểm chống gian lận hồ sơ.
* **AI Confidence Score (%):** Thanh tiến trình trực quan hiển thị độ tự tin thẩm định cấu trúc của mô hình. Độ tự tin tự động sụt giảm mạnh xuống mức 65% - 70% nếu phát hiện ra các dấu hiệu dữ liệu bất thường hoặc nằm trong vùng rủi ro trung bình.

---

## 7. ⚖️ Thiết kế giao diện Dashboard điều hành (Human-In-The-Loop)

Giao diện người dùng được tổ chức theo mô hình duyệt tác vụ tập trung trực quan chuyên nghiệp:

1.  **Tab 1 - Thẩm định đơn lẻ:** Cho phép upload bộ tài liệu thành phần trực tiếp của một sinh viên để AI phân tích chuyên sâu tức thì.
2.  **Tab 2 - Xét duyệt hàng loạt (Batch Review):** Nơi cán bộ nạp file danh sách Excel tổng hợp. Hệ thống tích hợp bộ sinh mã đợt duyệt tự động `batch_id` kèm theo nhãn thời gian thực (Ví dụ: `BATCH_0529_A3B5`) giúp cán bộ có thể dùng menu dropdown để lọc hiển thị riêng từng đợt duyệt của từng khoa/trường gửi lên một cách độc lập.
3.  **Khung hàng đợi (Queue Panel - Cột trái):** Liệt kê toàn bộ danh sách sinh viên dưới dạng danh sách chọn, hiển thị kèm nhãn trạng thái sơ bộ ban đầu của Rule Engine (`[PASS]` hoặc `[FAIL]`) giúp định vị nhanh ứng viên.
4.  **Trạm thanh tra chuyên sâu (Inspector Panel - Cột phải):** Khi cán bộ click vào một sinh viên bên hàng đợi, cột phải sẽ hiển thị toàn bộ biên bản lập luận từ AI Agent, các thanh màu đo lường rủi ro, và in ra các cờ cảnh báo gian lận.
5.  **Form phê duyệt tối hậu:** Tích hợp nút bấm radio cho phép con người đưa ra quyết định đóng hồ sơ sau cùng (`APPROVED` - Duyệt cấp danh hiệu, `REJECTED` - Bác bỏ, `MANUAL_REVIEW` - Cần đưa ra họp Hội đồng) cùng khung nhập ghi chú lý do hành chính, lưu đồng bộ xuống CSDL và làm mới trang web bằng lệnh `st.rerun()` an toàn.

---

## 8. 🌐 Kế hoạch tích hợp hạ tầng API Ban tổ chức (Phase 5 Roadmap)

Hệ thống hiện tại đã hoàn thiện mô hình MVP Vòng 2. Kiến trúc mã nguồn được thiết kế dạng Module cô lập (Adapter Design Pattern) giúp hệ thống sẵn sàng cắm rút và đấu nối trực tiếp vào hạ tầng API của **VNPT AI** khi được Ban tổ chức cung cấp tài liệu kỹ thuật:

```text
       [Tài liệu minh chứng gốc] (PDF / Ảnh chụp bảng điểm, chứng chỉ)
                     │
                     ▼ (Đọc file nhị phân Bytes đưa vào api_client.py)
         [VNPT SmartReader OCR API]
                     │
                     ▼ (Thu hồi văn bản thô - Raw Text Layer)
           [Normalizer Adapter]
                     │
                     ▼ (Chuẩn hóa cấu trúc thực thể đưa về JSON sạch)
  [Hệ thống Rule Engine & SQLite DB nội bộ của bạn chạy ổn định]
                     │
                     ▼ (Truyền chuỗi văn bản đã làm sạch)
      [VNPT Smartbot / VNPT LLM API] ──► Biên bản giải trình & Reviewer UI
```

---

## 9. 🚀 Hướng dẫn khởi chạy hệ thống (1-Lệnh Duy Nhất)

### Bước 1: Khởi tạo môi trường ảo và cài đặt thư viện
Mở Terminal tại thư mục gốc của dự án và thực thi lệnh:
```bash
pip install -r requirements.txt
```

### Bước 2: Đồng bộ hóa cơ sở dữ liệu vật lý
Chạy file khởi tạo để SQLAlchemy xây dựng cấu trúc file CSDL `sv5tot.db` chuẩn xác bên trong thư mục `backend`:
```bash
python backend/init_db.py
```
Màn hình xuất hiện dòng chữ `Database initialized` là thành công.

### Bước 3: Khởi chạy giao diện điều hành Dashboard
Gõ lệnh để kích hoạt giao diện Web Streamlit trên trình duyệt:
```bash
streamlit run frontend/app.py
```
Hệ thống sẽ tự động mở trang web quản trị tại địa chỉ mặc định `http://localhost:8501`. Bạn đã sẵn sàng nạp file Excel danh sách thử nghiệm để trải nghiệm toàn bộ luồng xử lý tự động hóa của hệ thống!