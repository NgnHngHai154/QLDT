# Work Board

| Area / UC | Owner | Status | Dependency / Notes |
|---|---|---|---|
| FE shell / UC001 | Frontend | Completed | Đăng nhập/xác thực khớp FastAPI `accessToken` và nested `user` |
| FE UC002 | Frontend | Completed | Catalog công khai đọc có phân trang từ BE; admin CRUD môn/lớp và chỉnh lịch phân công lưu qua API, không dùng mock |
| FE UC003/UC009 | Frontend | Completed | Bảng danh sách sinh viên của lớp học phần (`SectionRosterPage`) hiển thị MSSV, họ tên, email, khóa, ngành, thời điểm đăng ký |
| FE UC005 | Frontend | Completed | Đăng ký học phần theo kỳ hiện tại, xử lý các mã lỗi nghiệp vụ (`CLASS_FULL`, `SAME_SUBJECT_REGISTERED`, `STUDENT_SCHEDULE_CONFLICT`, `CREDIT_LIMIT_EXCEEDED`) |
| FE UC006 | Frontend | Completed | Hủy đăng ký học phần, cảnh báo nếu dưới ngưỡng tín chỉ tối thiểu (`CREDIT_LIMIT_BELOW_MIN`) |
| FE UC007/UC008 | Frontend | Completed | Thời khóa biểu tuần cho sinh viên và lịch giảng dạy cho giảng viên, tự động theo kỳ duy nhất |
| BE Auth / UC001 | Backend | Completed | FastAPI auth JWT, kiểm tra mật khẩu bcrypt, RBAC đầy đủ |
| BE Catalog / UC002 | Backend | Completed | CRUD môn học và lớp học phần, kiểm tra trùng lịch phòng/giảng viên |
| BE Registration / UC005, UC006 | Backend | Completed | Đăng ký/hủy học phần, khóa dòng học sinh FOR UPDATE, tính tín chỉ theo kỳ, cập nhật sĩ số nguyên tử |
| BE Timetable / UC007, UC008 | Backend | Completed | API thời khóa biểu sinh viên & lịch dạy giảng viên, tự động nhận diện tuần học |
| BE Timetable conflicts | Backend | Completed | Engine chung phân loại xung đột sinh viên/phòng/giảng viên theo tiết và tuần giao nhau; cập nhật lớp trả chi tiết sinh viên bị ảnh hưởng |
| BE Tuition & receipts | Backend | Completed | Đơn giá hiệu lực, TCHP, miễn giảm, đợt nộp, hóa đơn, thanh toán giả lập idempotent, snapshot biên lai và PDF |
| BE Roster / UC003, UC009 | Backend | Completed | API danh sách sinh viên theo lớp học phần với kiểm tra quyền truy cập |
| API/OpenAPI | Contracts | Completed | `contracts/openapi.yaml` và `contracts/api-types.ts` bao gồm routes/DTO thời khóa biểu và học phí |
| Database seed | Database | Completed | `db/seed/seed.sql` đã cập nhật 1 kỳ duy nhất (2026.1), 400 lớp học phần thuộc kỳ 2026.1 |
| Testing / Feature 10 + Tuition | Testing | Completed | Backend suite: 66 passed, 7 integration tests skipped; thêm API, PDF, tính học phí và conflict tests |
| CI/CD & Quality | DevOps | Completed | Backend pytest/Ruff pass; Alembic upgrade/check trên SQLite pass; frontend không thuộc phạm vi thay đổi |

Current verification: 66 backend tests pass, 7 MySQL/gateway/frontend integration tests remain skipped by default, Ruff passes, Alembic upgrade/check and legacy-rate backfill pass on SQLite, and Compose configuration is valid. OpenAPI paths and schema references match the runtime app. Frontend was not modified or rebuilt; MySQL concurrency and PDF rendering inside Docker remain unverified.
