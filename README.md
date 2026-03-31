VIDEO Chạy Demo App em để ở đây:

Demo app: [https://drive.google.com/drive/folders/1gH2ZIfpWoqMZBdc8BMCq7OsECumnk4Pv](https://drive.google.com/file/d/1eukH4z5pOY032FbhaBfTaiBbS8gAUDj6/view?usp=sharing)
em cập nhật lại tài khoản hệ thống là: 
User: Ken / 111111
Admin: KKK / 123456
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

Hệ thống được thiết kế theo mô hình kiến trúc 3 tầng nhằm đảm bảo tính tổ chức, dễ bảo trì và mở rộng:

Tầng giao diện (Frontend)
- Được xây dựng bằng Python Tkinter
-- Cung cấp giao diện cho người dùng:
  - Nhập văn bản
  - Chọn ngôn ngữ
  - Sử dụng dịch giọng nói
  - Dịch từ hình ảnh
  - Hiển thị kết quả dịch

Tầng xử lý (Backend)
- Xử lý toàn bộ logic nghiệp vụ của hệ thống, bao gồm:
  - Gọi API dịch bằng thư viện googletrans
  - Nhận diện giọng nói bằng speech_recognition
  - Chuyển văn bản thành giọng nói bằng gTTS
  - Nhận diện ký tự từ hình ảnh bằng EasyOCR
  - Xử lý đa luồng với threading để tránh treo giao diện

Tầng dữ liệu (Database)
- Sử dụng SQLite để lưu trữ dữ liệu:
  - Thông tin người dùng
  - Lịch sử dịch
  - Phản hồi và đánh giá

Lưu trữ thông tin người dùng và lịch sử dịch.

### 6.2 Luồng xử lý hệ thống
<img width="1057" height="692" alt="image" src="https://github.com/user-attachments/assets/cc00aa5c-6691-4a0b-af49-ce0107a6c135" />

Dịch văn bản

  - 1.Người dùng nhập văn bản
  - 2.Chọn ngôn ngữ nguồn và đích
  - 3.Hệ thống gửi yêu cầu đến API dịch
  - 4.Nhận kết quả và hiển thị
  - 
Dịch giọng nói

  - 1.Thu âm từ microphone
  - 2.Chuyển giọng nói thành văn bản
  - 3.Gửi văn bản đi dịch
  - 4.Hiển thị và đọc kết quả
  - 
Dịch hình ảnh

  - 1.Người dùng chọn ảnh
  - 2.OCR trích xuất văn bản
  - 3.Gửi nội dung đi dịch
  - 4.Hiển thị kết quả

Ví dụ quy trình xử lý dịch:

- 1.Người dùng nhập văn bản hoặc chọn chức năng "Voice Translate"
- 2.Hệ thống tiếp nhận dữ liệu đầu vào (văn bản hoặc giọng nói)
- 3.Thực hiện xử lý và dịch sang ngôn ngữ đích
- 4.Lưu kết quả vào cơ sở dữ liệu
- 5.Hiển thị kết quả lên giao diện
- 6.(Tùy chọn) Phát âm nội dung đã dịch

6.3 
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

USERS – FEEDBACK:
Một người dùng có thể gửi nhiều phản hồi.
→ Quan hệ: 1 - N

7.4 Sơ đồ ERD

<img width="1056" height="549" alt="image" src="https://github.com/user-attachments/assets/9383eae2-37d4-4fb5-a187-8fb7a4be2a64" />

# 8. CÀI ĐẶT VÀ HƯỚNG DẪN SỬ DỤNG

## 8.1 Yêu cầu hệ thống

Để chạy được ứng dụng, cần đảm bảo các yêu cầu sau:

- Hệ điều hành: Windows / Linux / macOS
- Python phiên bản: >= 3.8
- Kết nối Internet (bắt buộc cho các chức năng dịch và nhận diện giọng nói)
- Microphone (đối với chức năng Voice Translate)

## 8.2 Cài đặt môi trường

- Bước 1: Clone repository về máy

  git clone https://github.com/Khang226000/language-translator.git
  cd language-translator

- Bước 2: Cài đặt thư viện cần thiết
  
  pip install -r requirements.txt

  Hoặc cài thủ công:
  
  pip install googletrans==4.0.0-rc1
  
  pip install speechrecognition
  
  pip install gtts
  
  pip install easyocr
  
  pip install pillow
  
  pip install opencv-python
  
  pip install pyaudio

## 8.3 Chạy ứng dụng

  - Chạy file chính: python main.py

## 8.4 Hướng dẫn sử dụng

Sau khi chạy ứng dụng, người dùng có thể:

- Nhập văn bản vào ô nhập → chọn ngôn ngữ → nhấn nút Dịch
- Nhấn nút Voice để nhập bằng giọng nói
- Nhấn nút Image để chọn ảnh và dịch nội dung
- Nhấn nút loa để nghe phát âm
- Sử dụng các chức năng:
- Copy kết quả
- Xóa nội dung
- Đảo ngôn ngữ
  
# 9. Phân tích API và AI tích hợp trong hệ thống

## 9.1 Tổng quan

- Hệ thống dịch văn bản tích hợp nhiều API và công nghệ AI nhằm nâng cao khả năng xử lý ngôn ngữ tự nhiên, nhận dạng giọng nói và xử lý hình ảnh. Các thành phần này giúp hệ thống hoạt động thông minh, linh hoạt và gần với các ứng dụng thực tế hiện nay.

## 9.2 API dịch ngôn ngữ

- Hệ thống sử dụng thư viện googletrans để thực hiện chức năng dịch văn bản.

Cách hoạt động:

- Gửi văn bản nguồn lên dịch vụ Google Translate
- Nhận kết quả dịch trả về
- Hiển thị cho người dùng

Ưu điểm:

- Hỗ trợ nhiều ngôn ngữ
- Tốc độ xử lý nhanh
- Độ chính xác cao đối với văn bản phổ thông

Hạn chế:

- Phụ thuộc vào kết nối Internet
- Có thể bị giới hạn request
- Không tối ưu cho văn bản chuyên ngành
  
## 9.3 AI nhận diện giọng nói (Speech Recognition)

Hệ thống sử dụng thư viện speech_recognition để chuyển giọng nói thành văn bản.

Quy trình xử lý:

- 1.Thu âm từ microphone
- 2.Gửi dữ liệu âm thanh đến dịch vụ nhận dạng
- 3.Chuyển đổi thành văn bản
- 4.Đưa vào hệ thống dịch

Ứng dụng AI:

- Nhận dạng giọng nói dựa trên mô hình học máy
- Xử lý ngôn ngữ tự nhiên (NLP)

Ưu điểm:

- Tăng tính tiện lợi khi nhập liệu
- Hỗ trợ người dùng không cần gõ văn bản

Hạn chế:

- Phụ thuộc chất lượng microphone
- Dễ sai với tiếng ồn hoặc giọng địa phương
  
## 9.4 AI chuyển văn bản thành giọng nói (Text-to-Speech)

Hệ thống sử dụng gTTS để chuyển văn bản thành âm thanh.

Cách hoạt động:

- Nhận văn bản đầu vào
- Gửi đến dịch vụ chuyển đổi giọng nói
- Trả về file âm thanh (.mp3)
- Phát cho người dùng

Ứng dụng:

- Hỗ trợ luyện nghe
- Hỗ trợ phát âm chuẩn
  
## 9.5 AI nhận diện văn bản từ hình ảnh (OCR)

Hệ thống sử dụng EasyOCR để trích xuất văn bản từ hình ảnh.

Quy trình:

- 1.Người dùng chọn ảnh
- 2.Hệ thống phân tích ảnh
- 3.Nhận diện ký tự trong ảnh
- 4.Chuyển thành văn bản
- 5.Thực hiện dịch

Công nghệ sử dụng:

- Deep Learning (CNN)
- Computer Vision

Ưu điểm:

- Hỗ trợ dịch tài liệu, ảnh chụp
- Tăng khả năng xử lý đa dạng dữ liệu

Hạn chế:

- Độ chính xác phụ thuộc chất lượng ảnh
- Khó nhận diện chữ viết tay
  
## 9.6 Xử lý đa luồng (Multithreading)

Hệ thống sử dụng threading để xử lý song song:

- Tránh treo giao diện khi gọi API
- Tăng trải nghiệm người dùng
- Cho phép thực hiện nhiều tác vụ cùng lúc

9.7 Đánh giá tổng thể

Việc tích hợp API và AI giúp hệ thống đạt được:

- Khả năng xử lý đa phương thức (text, voice, image)
- Tăng độ tiện lợi và trải nghiệm người dùng
- Tiệm cận các ứng dụng dịch thuật hiện đại

-> Tuy nhiên, hệ thống vẫn còn phụ thuộc vào:

- 1.Kết nối Internet
- 2.Dịch vụ bên thứ ba
- 3.Giới hạn của các mô hình AI có sẵn
