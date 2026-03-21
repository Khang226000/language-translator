Demo app: https://drive.google.com/drive/folders/1gH2ZIfpWoqMZBdc8BMCq7OsECumnk4Pv
# HỆ THỐNG DỊCH VĂN BẢN (LANGUAGE TRANSLATOR)

## 1. Giới thiệu

Trong bối cảnh hội nhập quốc tế và sự phát triển mạnh mẽ của công nghệ thông tin, nhu cầu giao tiếp và trao đổi thông tin giữa các ngôn ngữ ngày càng gia tăng. Tuy nhiên, rào cản ngôn ngữ vẫn là một trong những khó khăn lớn, ảnh hưởng đến việc học tập, làm việc và tiếp cận tri thức của con người.

Để giải quyết vấn đề này, đề tài “Hệ thống dịch văn bản” được thực hiện nhằm xây dựng một ứng dụng hỗ trợ dịch ngôn ngữ một cách nhanh chóng, chính xác và tiện lợi. Hệ thống không chỉ cung cấp chức năng dịch văn bản truyền thống mà còn tích hợp nhiều công nghệ hiện đại như nhận dạng giọng nói, chuyển văn bản thành giọng nói và nhận dạng ký tự từ hình ảnh.

Ứng dụng được phát triển dưới dạng phần mềm Desktop sử dụng ngôn ngữ lập trình Python, hướng đến đối tượng người dùng là sinh viên, người học ngoại ngữ và nhân viên văn phòng.

---

## 2. Mục tiêu của hệ thống

Hệ thống được xây dựng với các mục tiêu chính như sau:

- Cung cấp công cụ dịch văn bản đa ngôn ngữ nhanh chóng và chính xác.
- Xây dựng giao diện thân thiện, dễ sử dụng cho mọi đối tượng người dùng.
- Hỗ trợ nhập liệu linh hoạt thông qua văn bản, giọng nói và hình ảnh.
- Tích hợp chức năng chuyển văn bản thành giọng nói nhằm hỗ trợ luyện nghe và phát âm.
- Cho phép người dùng xử lý thông tin từ nhiều nguồn khác nhau như văn bản, tài liệu, hình ảnh.
- Đảm bảo hệ thống hoạt động ổn định, có khả năng mở rộng và nâng cấp trong tương lai.

---

## 3. Phạm vi ứng dụng

Hệ thống dịch văn bản được áp dụng trong các trường hợp sau:

- Hỗ trợ học tập ngoại ngữ cho học sinh, sinh viên.
- Phục vụ nhu cầu dịch thuật trong công việc và đời sống.
- Hỗ trợ người dùng tiếp cận tài liệu nước ngoài.
- Hỗ trợ luyện kỹ năng nghe và phát âm thông qua chức năng Text-to-Speech.

Phạm vi triển khai:
- Ứng dụng Desktop chạy trên máy tính cá nhân.
- Không yêu cầu cấu hình phần cứng cao.
- Một số chức năng yêu cầu kết nối Internet (dịch trực tuyến, nhận dạng giọng nói).

---

## 4. Tổng quan chức năng hệ thống

Hệ thống cung cấp các nhóm chức năng chính bao gồm:

### 4.1 Dịch văn bản
Cho phép người dùng nhập nội dung văn bản và thực hiện dịch sang ngôn ngữ mong muốn một cách nhanh chóng.

### 4.2 Dịch bằng giọng nói
Người dùng có thể sử dụng microphone để nhập liệu bằng giọng nói. Hệ thống sẽ:
- Nhận dạng giọng nói
- Chuyển thành văn bản
- Thực hiện dịch
- Hiển thị và đọc kết quả

### 4.3 Chuyển văn bản thành giọng nói
Hỗ trợ đọc nội dung văn bản sau khi dịch, giúp người dùng luyện kỹ năng nghe và phát âm.

### 4.4 Dịch văn bản từ hình ảnh
Sử dụng công nghệ OCR để trích xuất nội dung văn bản từ hình ảnh và thực hiện dịch.

### 4.5 Quản lý dữ liệu người dùng
- Đăng ký, đăng nhập tài khoản
- Lưu lịch sử dịch
- Quản lý thông tin cá nhân

### 4.6 Chức năng quản trị hệ thống
- Quản lý người dùng
- Phân quyền
- Thống kê dữ liệu
- Xuất báo cáo

---

## 5. Ý nghĩa của hệ thống

Việc phát triển hệ thống dịch văn bản mang lại nhiều lợi ích:

- Giúp tiết kiệm thời gian trong quá trình dịch thuật.
- Hỗ trợ học tập và nghiên cứu tài liệu nước ngoài.
- Nâng cao hiệu quả làm việc trong môi trường đa ngôn ngữ.
- Tăng khả năng tiếp cận tri thức toàn cầu.
- Góp phần ứng dụng công nghệ hiện đại vào đời sống thực tiễn.

## 6. KIẾN TRÚC HỆ THỐNG

Hệ thống được thiết kế theo mô hình phân lớp nhằm đảm bảo tính rõ ràng, dễ bảo trì và mở rộng trong tương lai.

### 6.1 Mô hình tổng thể

Hệ thống bao gồm 4 lớp chính:

Presentation Layer (Giao diện người dùng)
Xây dựng bằng Tkinter, cho phép người dùng tương tác với hệ thống thông qua các chức năng như nhập văn bản, chọn ngôn ngữ, hiển thị kết quả.
Business Logic Layer (Xử lý nghiệp vụ)
Xử lý toàn bộ logic của hệ thống như:
Xử lý yêu cầu dịch
Điều phối dữ liệu giữa giao diện và dịch vụ
Kiểm tra dữ liệu đầu vào
Service Layer (Dịch vụ bên ngoài)
Kết nối với các API và thư viện:
Google Translate (dịch văn bản)
Speech Recognition (nhận dạng giọng nói)
EasyOCR (nhận dạng ký tự từ hình ảnh)
Data Layer (Tầng dữ liệu)
Lưu trữ thông tin người dùng và lịch sử dịch.

### 6.2 Luồng xử lý hệ thống
<img width="1057" height="692" alt="image" src="https://github.com/user-attachments/assets/cc00aa5c-6691-4a0b-af49-ce0107a6c135" />

Dịch văn bản
  - 1.Người dùng nhập văn bản
  - 2.Chọn ngôn ngữ nguồn và đích
  - 3.Hệ thống gửi yêu cầu đến API dịch
  - 4.Nhận kết quả và hiển thị
Dịch giọng nói
  - 1.Thu âm từ microphone
  - 2.Chuyển giọng nói thành văn bản
  - 3.Gửi văn bản đi dịch
  - 4.Hiển thị và đọc kết quả
Dịch hình ảnh
  - 1.Người dùng chọn ảnh
  - 2.OCR trích xuất văn bản
  - 3.Gửi nội dung đi dịch
  - 4.Hiển thị kết quả

7. Thiết kế cơ sở dữ liệu

Hệ thống sử dụng cơ sở dữ liệu để lưu trữ thông tin người dùng, lịch sử dịch, phân quyền và các dữ liệu liên quan. Thiết kế cơ sở dữ liệu đảm bảo tính toàn vẹn, dễ mở rộng và phù hợp với mô hình ứng dụng.

7.1 Danh sách các bảng

Hệ thống bao gồm các bảng chính sau:

- USERS: Lưu thông tin người dùng
- ROLES: Lưu vai trò (Admin, User)
- HISTORY: Lưu lịch sử dịch
- SOCIAL_ACCOUNTS: Lưu thông tin đăng nhập mạng xã hội
- EEDBACK: Lưu phản hồi từ người dùng

7.2 Mô tả chi tiết các bảng

USERS
- id (INTEGER, PRIMARY KEY)
- username (TEXT)
- password (TEXT)
- email (TEXT)
- role_id (INTEGER, FOREIGN KEY)
- created_at (DATETIME)
- ROLES
- id (INTEGER, PRIMARY KEY)
- role_name (TEXT)
  
HISTORY
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER, FOREIGN KEY)
- source_text (TEXT)
- translated_text (TEXT)
- source_lang (TEXT)
- target_lang (TEXT)
- created_at (DATETIME)
  
SOCIAL_ACCOUNTS
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER, FOREIGN KEY)
- provider (TEXT)
- provider_user_id (TEXT)
  
FEEDBACK
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER, FOREIGN KEY)
- content (TEXT)
- created_at (DATETIME)

7.3 Mối quan hệ giữa các bảng

USERS – ROLES:
- Một vai trò có thể được gán cho nhiều người dùng, mỗi người dùng chỉ có một vai trò.
→ Quan hệ: 1 - N

USERS – HISTORY:
- Một người dùng có thể có nhiều lịch sử dịch, mỗi lịch sử thuộc về một người dùng.
→ Quan hệ: 1 - N

USERS – SOCIAL_ACCOUNTS:
- Một người dùng có thể liên kết nhiều tài khoản mạng xã hội.
→ Quan hệ: 1 - N

7.4 Sơ đồ ERD

<img width="1056" height="549" alt="image" src="https://github.com/user-attachments/assets/9383eae2-37d4-4fb5-a187-8fb7a4be2a64" />

USERS – FEEDBACK:
Một người dùng có thể gửi nhiều phản hồi.
→ Quan hệ: 1 - N

