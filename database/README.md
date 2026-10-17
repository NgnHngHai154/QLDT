# Cơ sở dữ liệu QLDT

Cấu trúc CSDL và dữ liệu mẫu cho hệ thống Quản lý & Đăng ký Học phần Trực tuyến.
Thiết kế theo *Tài liệu thiết kế phần mềm v1.0* (mục 3) và *Quy ước API và JSON v1.0* (mục 3.2).

## Cách nạp

Yêu cầu MySQL 8.0.16 trở lên (cần cho ràng buộc `CHECK` của bảng `COURSE_SECTIONS`).

```bash
mysql -u root -p < schema.sql
mysql -u root -p < seed.sql
```

Sau khi chạy sẽ có database `qldt`. `seed.sql` xóa dữ liệu cũ trước khi nạp nên có thể chạy lại nhiều lần.

## Tài khoản thử

Mật khẩu lưu dạng băm bcrypt, tương thích `BCryptPasswordEncoder` của Spring. Tài khoản `admin` dùng mật khẩu `admin`, giảng viên và sinh viên dùng chung mật khẩu `123456`. Cần đổi mật khẩu admin khi triển khai thật.

| Vai trò | Tên đăng nhập | Mã riêng |
|---|---|---|
| Quản trị | `admin` | không có |
| Giảng viên | `gv001` đến `gv010` | `GV001` đến `GV010` |
| Sinh viên | `sv20210001` đến `sv20211000` | `20210001` đến `20211000` |

Tên đăng nhập của sinh viên là `sv` cộng với mã số sinh viên.

## Dữ liệu mẫu

| Bảng | Số bản ghi |
|---|---|
| `USERS` | 1011 (1 quản trị, 10 giảng viên, 1000 sinh viên) |
| `LECTURERS` | 10 |
| `STUDENTS` | 1000 (khóa K66) |
| `SUBJECTS` | 100 |
| `SEMESTERS` | 3 (`2025.1`, `2025.2`, `2026.1`) |
| `ROOMS` | 30 |
| `COURSE_SECTIONS` | 400, chia đều cho 3 học kỳ, `current_enrollment` = 0 |
| `REGISTRATIONS` | 0 (để trống, đăng ký khi chạy thực) |

Học kỳ hiện tại là `2026.1` (bắt đầu 07/09/2026), tương ứng `semester_id = 3`.
Mỗi giảng viên có lớp ở cả 3 học kỳ.

## Các bảng

- `USERS`: tài khoản đăng nhập của cả ba vai trò (ADMIN, LECTURER, STUDENT).
- `STUDENTS`, `LECTURERS`: hồ sơ riêng, liên kết 1-1 với `USERS`.
- `COURSE_SECTIONS`: bảng trung tâm, liên kết `SUBJECTS`, `SEMESTERS`, `ROOMS` và `LECTURERS`.
- `REGISTRATIONS`: liên kết nhiều-nhiều giữa `STUDENTS` và `COURSE_SECTIONS`.
- `SUBJECTS`, `SEMESTERS`, `ROOMS`: các bảng danh mục.

## Quy ước đặt tên

Tên bảng và cột trong CSDL dùng `snake_case` (ví dụ `student_code`), còn trường JSON trả về cho
front-end dùng `camelCase` (ví dụ `studentCode`). Bảng đối chiếu ở mục 3.2 của Quy ước API.
