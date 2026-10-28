# Feature 10 — Kiểm thử quản trị đào tạo và bộ dữ liệu thử nghiệm

## 1. Mục tiêu và phạm vi

Feature 10 (Sprint 2) xác minh chức năng quản trị đào tạo từ giao diện đến cơ sở dữ liệu:

- UC002: quản trị môn học, lớp học phần, phân công giảng viên/phòng và kiểm tra trùng lịch.
- UC003: xem danh sách sinh viên của lớp học phần (dùng chung với UC009 cho giảng viên).
- Kết nối FE–BE–DB, quy trình chạy local và bộ dữ liệu thử nghiệm có thể tái lập.
- Kịch bản kiểm thử tự động bằng `pytest`, gồm cả kiểm thử tích hợp với MySQL thật.

Nghiệp vụ đã chốt: hệ thống **không** còn ràng buộc môn tiên quyết/song hành. API dùng JSON
camelCase; object trả về dùng `id`, request tham chiếu dùng `subjectId`, `sectionId`,
`semesterId`, `lecturerId`, `roomId`. Chi tiết tại `docs/api-conventions.md` và
`contracts/openapi.yaml`.

## 2. Hạng mục bàn giao

| Hạng mục | Vị trí |
|---|---|
| Bộ dữ liệu thử nghiệm | `backend/scripts/seed_test_data.py` |
| Kiểm thử API quản trị (SQLite, chạy mặc định) | `backend/tests/test_admin_training.py` |
| Kiểm thử tích hợp FE–BE–DB (MySQL + gateway + frontend) | `backend/tests/integration/` |
| Hướng dẫn chạy và checklist thủ công | tài liệu này |

Kiểm thử không thay đổi schema hay hợp đồng API.

## 3. Yêu cầu môi trường

- Python 3.12+ và `pip`.
- Node.js 20+ và `npm`.
- Docker Engine cùng Docker Compose plugin (`docker compose version`).
- MySQL 8.4 chạy qua container; không cần cài MySQL trên máy host.
- Các lệnh bên dưới chạy từ thư mục gốc repo. Trên Linux/macOS dùng `python3`/`source`,
  trên Windows dùng `python`/`.\.venv\Scripts\Activate.ps1`.

Chỉ dùng mật khẩu và dữ liệu mẫu trong môi trường local. Không nạp bộ dữ liệu thử nghiệm
lên database dùng chung hoặc production.

## 4. Khởi động FE–BE–DB

### 4.1. Cấu hình

```bash
cp .env.example .env
```

Cập nhật `MYSQL_PASSWORD`, `MYSQL_ROOT_PASSWORD` và `JWT_SECRET` (tối thiểu 32 ký tự) trong
`.env`. File này nằm ở gốc repo và đã được gitignore.

### 4.2. Cách A — backend chạy trên máy host (phù hợp kiểm thử FE)

```bash
# Terminal 1: MySQL
docker compose up -d db

# Terminal 2: backend
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head
python -m scripts.seed
python -m scripts.seed_test_data
uvicorn app.main:app --reload
```

```bash
# Terminal 3: frontend
cd frontend
npm install
npm run dev
```

Địa chỉ:

- Frontend: `http://localhost:5173` (Vite proxy `/api` tới `http://127.0.0.1:8000`).
- Backend: `http://localhost:8000`; Swagger: `http://localhost:8000/api/docs`; health: `/health`.
- MySQL: `127.0.0.1:3306`.

### 4.3. Cách B — stack API qua Docker Compose và gateway

```bash
docker compose up -d --build db
docker compose run --rm backend alembic upgrade head
docker compose run --rm backend python -m scripts.seed
docker compose run --rm backend python -m scripts.seed_test_data
docker compose up -d --build backend gateway
python gateway/smoke_test.py
```

Địa chỉ: gateway `http://localhost:8080`; Swagger `http://localhost:8080/api/docs`;
health `http://localhost:8080/health`; kiểm tra gateway → backend: `/health/backend`.

Frontend vẫn chạy riêng bằng `npm run dev` (Compose chưa bật service frontend). Gateway
trong Compose chỉ gọi được backend nếu backend nằm trong cùng network hoặc có địa chỉ
truy cập được từ container. Cách ổn định nhất là dùng Cách B ở trên; nếu backend chạy
ngoài Compose, cấu hình `BACKEND_URL` trỏ tới địa chỉ mà container gateway truy cập được.

## 5. Bộ dữ liệu thử nghiệm

Script idempotent, chỉ tác động bản ghi có tiền tố `TST`/`TGV`/`TSV`:

```bash
cd backend
source .venv/bin/activate

python -m scripts.seed_test_data           # tạo hoặc cập nhật
python -m scripts.seed_test_data --reset   # xóa rồi tạo lại
python -m scripts.seed_test_data --cleanup # chỉ xóa
```

Dữ liệu chính (học kỳ `2026.1`):

| Nhóm | Bản ghi |
|---|---|
| Phòng | `TST-101` (60 chỗ), `TST-102` (20 chỗ) |
| Môn học | `TST101` (3 TC), `TST102` (4 TC), `TST103` (3 TC), `TST104` (2 TC) |
| Giảng viên | `testgv001` / `TGV001`, `testgv002` / `TGV002` |
| Sinh viên | `testsv001` / `T20260001`, `testsv002` / `T20260002`, `testsv003` / `T20260003` |
| Lớp học phần | `TST-S01` … `TST-S05` |
| Tài khoản | `testgv001/123456`, `testgv002/123456`, `testsv001/123456`, `testsv002/123456`, `testsv003/123456` |

Các lớp được thiết kế cho checklist:

- `TST-S01`: nhiều sinh viên, còn chỗ (dùng kiểm tra roster và hủy đăng ký).
- `TST-S03`: sức chứa 1 và đã đầy (dùng kiểm tra `CLASS_FULL`).
- `TST-S05`: lớp trống cùng môn `TST101` (dùng kiểm tra `SAME_SUBJECT_REGISTERED` khi sinh viên
  đã có `TST-S01`).
- `TST-S02`/`TST-S04`: các môn và khung giờ khác nhau, không trùng phòng/giảng viên.

Script kiểm tra trùng phòng và trùng giảng viên trước khi commit; nếu phát hiện sẽ dừng và
không ghi dữ liệu. Chạy `--cleanup` sau khi thử nghiệm xong nếu không muốn giữ dữ liệu.

## 6. Chạy kiểm thử

### 6.1. Kiểm thử API mặc định (không cần MySQL)

```bash
cd backend
source .venv/bin/activate
ruff check .
pytest
```

`pytest` dùng SQLite trong bộ nhớ. Các test Feature 10 nằm trong
`tests/test_admin_training.py` và bao phủ:

- Đọc lookups, học kỳ hiện tại và phân trang môn/lớp.
- RBAC: sinh viên/giảng viên không được CRUD môn/lớp hoặc xem lookups quản trị.
- Môn học: tạo, trùng mã, tìm kiếm, chi tiết, cập nhật, chặn xóa khi còn lớp, xóa thành công.
- Validation camelCase: `subjectCode`, `name`, `credits`.
- Lớp học phần: tạo, trường response (`subject`, `semester`, `lecturer`, `room`,
  `currentEnrollment`, `remainingSeats`, `full`, `registeredByMe`), cập nhật, xóa.
- Tham chiếu không tồn tại (`subjectId`, `semesterId`, `lecturerId`, `roomId`).
- Trùng mã lớp, tiết/tuần không hợp lệ, vượt sức chứa phòng, thứ không hợp lệ.
- Trùng lịch phòng và trùng lịch giảng viên (`SCHEDULE_CONFLICT`).
- Giảm sức chứa dưới sĩ số (`CAPACITY_BELOW_ENROLLMENT`), đổi môn/học kỳ khi đã có đăng ký
  (`SECTION_HAS_REGISTRATIONS`), chặn xóa lớp đã có đăng ký.
- Roster: quyền admin/giảng viên phụ trách, từ chối giảng viên khác và sinh viên, payload
  `studentCode`/`fullName`/`email`/`cohort`/`major`/`registeredAt`.
- Đăng ký hai môn không có quan hệ tiên quyết/song hành vẫn thành công.
- Hợp đồng OpenAPI và `db/schema.sql` không chứa `prerequisite`/`corequisite`.

### 6.2. Kiểm thử tích hợp FE–BE–DB

Khởi động stack theo mục 4, nạp bộ dữ liệu theo mục 5, sau đó:

```bash
cd backend
source .venv/bin/activate
pytest -m integration
```

Các test tự bỏ qua nếu thiếu MySQL/backend/gateway/frontend. Biến môi trường tùy chọn:

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `QLDT_GATEWAY_URL` | `http://localhost:8080` | Gateway/API dùng cho test |
| `QLDT_FRONTEND_URL` | `http://localhost:5173` | Vite dev server |
| `QLDT_ADMIN_USERNAME` | `admin` | Tài khoản admin |
| `QLDT_ADMIN_PASSWORD` | `admin` | Mật khẩu admin seed |
| `QLDT_DATABASE_URL` | đọc từ `.env` gốc | URL SQLAlchemy tới MySQL |

Nếu chưa chạy gateway, có thể trỏ `QLDT_GATEWAY_URL=http://localhost:8000` cho các test API
và bỏ qua test gateway: `pytest -m integration -k "not gateway"`. Test frontend cần Vite và
backend mà Vite proxy trỏ tới (`127.0.0.1:8000`).

Nội dung kiểm thử tích hợp:

- Gateway `/health`, `/health/backend` và header `X-Request-Id`.
- Lookups quản trị khớp số lượng bảng `SUBJECTS`, `LECTURERS`, `ROOMS`, `SEMESTERS` trong MySQL.
- Tạo/sửa/xóa môn học qua API và đối chiếu trực tiếp bảng `SUBJECTS`.
- Tạo lớp, phát hiện trùng lịch, sửa lịch và xóa; đối chiếu `COURSE_SECTIONS`.
- Hai sinh viên đăng ký, roster và `current_enrollment` khớp bảng `REGISTRATIONS`.
- Frontend trả HTML và Vite proxy `/api/subjects` trả cùng `totalItems` với backend.
- Bộ dữ liệu Feature 10 hiển thị qua API (`TST101`, lớp `TST-S03` sức chứa 1).

### 6.3. Kiểm tra frontend

```bash
cd frontend
npm run build
```

## 7. Checklist kiểm thử thủ công trên giao diện

Đăng nhập `admin / admin` tại `http://localhost:5173/login`.

### 7.1. Môn học — `/app/subjects`

- [ ] Danh sách có phân trang, tìm theo mã/tên; cột “Lớp đã mở” đúng.
- [ ] “Thêm môn học” tạo môn mới; môn xuất hiện sau khi tải lại.
- [ ] Mã trùng báo lỗi `DUPLICATE_CODE`; mã/tên/tín chỉ trống hoặc không hợp lệ báo
      `VALIDATION_ERROR`.
- [ ] “Sửa” cập nhật tên/tín chỉ/mô tả; dữ liệu giữ nguyên sau reload.
- [ ] Nút “Xóa” bị khóa khi môn đang có lớp; xóa môn không có lớp thành công.

### 7.2. Lớp học phần — `/app/sections`

- [ ] Hiển thị đúng học kỳ hiện tại `2026.1`; tìm theo mã lớp/môn.
- [ ] “Mở lớp học phần” tạo lớp với môn, giảng viên, phòng, thứ, tiết, tuần, sĩ số.
- [ ] Tạo lớp trùng phòng hoặc trùng giảng viên trong cùng khung giờ báo `SCHEDULE_CONFLICT`.
- [ ] Sĩ số tối đa vượt sức chứa phòng báo `VALIDATION_ERROR` tại `maxCapacity`.
- [ ] Tiết kết thúc nhỏ hơn tiết bắt đầu, tuần kết thúc vượt số tuần học, thứ ngoài 2–8 báo lỗi.
- [ ] “Sửa” đổi phòng/lịch thành công; giảm sĩ số dưới số đã đăng ký báo
      `CAPACITY_BELOW_ENROLLMENT`.
- [ ] Đổi môn hoặc học kỳ của lớp đã có đăng ký báo `SECTION_HAS_REGISTRATIONS`.
- [ ] Xóa lớp chưa có đăng ký thành công; lớp đã có đăng ký báo `SECTION_HAS_REGISTRATIONS`.

### 7.3. Xếp lịch và phân công — `/app/timetable/manage`

- [ ] Đổi giảng viên/phòng/thời gian của lớp và lưu thành công.
- [ ] Tạo xung đột với lớp khác bị từ chối và thông báo đúng.
- [ ] Dữ liệu mới xuất hiện ở danh sách lớp và thời khóa biểu liên quan sau reload.

### 7.4. Danh sách sinh viên — `/app/sections/{id}/students`

Mở trực tiếp URL trên trình duyệt; bảng lớp học phần hiện chưa có nút dẫn tới roster.

- [ ] Admin mở roster của `TST-S01` thấy đúng MSSV, họ tên, email, khóa, ngành, thời điểm đăng ký.
- [ ] Sĩ số hiển thị khớp `currentEnrollment / maxCapacity`.
- [ ] Giảng viên phụ trách mở được roster; giảng viên khác nhận 403.
- [ ] Sinh viên không mở được roster quản trị (403).
- [ ] Sau khi sinh viên đăng ký/hủy, tải lại roster thấy sĩ số và danh sách thay đổi.

### 7.5. Đăng ký không có tiên quyết/song hành

- [ ] `testsv003` (chỉ có `TST-S01`) đăng ký được `TST-S04` (môn `TST104`) mà không cần môn
      tiên quyết/song hành.
- [ ] `testsv001` đăng ký `TST-S05` báo `SAME_SUBJECT_REGISTERED` do đã có `TST-S01` cùng môn;
      đây là quy tắc trùng môn, không phải tiên quyết/song hành.
- [ ] `testsv003` đăng ký `TST-S03` (đã đầy 1/1) báo `CLASS_FULL`.

## 8. Xử lý sự cố thường gặp

| Hiện tượng | Cách xử lý |
|---|---|
| `docker compose` báo không có lệnh | Cài Docker Compose plugin và kiểm tra `docker compose version` |
| Backend báo thiếu bảng | Chạy `alembic upgrade head` trước khi seed/khởi động |
| `seed_test_data` báo thiếu học kỳ `2026.1` | Chạy `python -m scripts.seed` trước |
| Test tích hợp bị skip | Kiểm tra MySQL/backend/gateway/frontend và các URL `QLDT_*` |
| Test tích hợp không thấy dữ liệu | Chạy `python -m scripts.seed_test_data` và kiểm tra đúng database trong `.env` |
| Vite proxy lỗi 502 | Backend phải chạy tại `127.0.0.1:8000` hoặc chỉnh proxy trong `frontend/vite.config.ts` |
| Cổng 3306/8000/8080/5173 bận | Dừng tiến trình cũ hoặc đổi cổng tương ứng và cập nhật URL test |

## 9. Tiêu chí hoàn thành

- `ruff check .` và `pytest` trong `backend/` đạt.
- `pytest -m integration` đạt khi stack và dữ liệu đã sẵn sàng (hoặc skip có lý do rõ ràng).
- `npm run build` trong `frontend/` đạt.
- Checklist mục 7 được thực hiện trên giao diện với bộ dữ liệu Feature 10.
- Không còn mã nguồn, hợp đồng API hoặc schema nào chứa tiên quyết/song hành.
