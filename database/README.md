# Dữ liệu CSDL — Hệ thống Đăng ký học phần

Thư mục này chứa cấu trúc cơ sở dữ liệu và một bộ dữ liệu mẫu để team bắt đầu code.
Dữ liệu mẫu sinh đúng theo *Tài liệu thiết kế phần mềm v1.0* (mục 3) và
*Quy ước API và JSON v1.0* (mục 3.2).

## Cách nạp

Cần **MySQL 8.0.16 trở lên** (bản cũ hơn không chạy được ràng buộc `CHECK` mà bảng
`COURSE_SECTIONS` dùng tới).

```bash
mysql -u root -p < schema.sql
mysql -u root -p < seed.sql
```

Sau đó có database tên `qldt`. Chạy `seed.sql` bao nhiêu lần cũng được — file tự xóa
dữ liệu cũ trước khi nạp.

## Đăng nhập thử

Mọi tài khoản dùng chung mật khẩu: **`123456`**

| Ai | Tài khoản | Mã riêng |
|---|---|---|
| Ban quản lý | `admin`, `admin02` | — |
| Giảng viên | `gv001` … `gv010` | `GV001` … `GV010` |
| Sinh viên | `sv20210001` … `sv20211000` | `20210001` … `20211000` |

Tên đăng nhập của sinh viên chính là chữ `sv` cộng với mã số sinh viên, nên nhìn
tài khoản là biết mã. Mật khẩu được lưu dạng băm bcrypt, khớp với `BCryptPasswordEncoder`
của Spring — đăng nhập thật được chứ không phải dữ liệu giả.

## Trong database có gì

- **10 giảng viên**, 1000 **sinh viên** (toàn bộ thuộc khóa K66 — đây là khóa duy nhất
  xuất hiện trong tài liệu, mục 7.6 của Quy ước API), **100 môn học**.
- **3 học kỳ**: `2025.1`, `2025.2`, `2026.1`. Học kỳ `2026.1` là học kỳ hiện tại
  (bắt đầu 07/09/2026) — khi code API `/api/semesters/current` thì `semester_id = 3`.
- **30 phòng học**, **400 lớp học phần** chia đều cho 3 học kỳ.
- Khoảng **12 nghìn** bản ghi đăng ký, mỗi sinh viên đăng ký 3–6 lớp mỗi học kỳ.

Mỗi giảng viên phụ trách lớp ở cả 3 học kỳ, nên màn hình "lịch dạy" của giảng viên
(UC008) có dữ liệu ngay.

## 8 bảng nói gì

`USERS` giữ tài khoản đăng nhập của cả ba vai trò. `STUDENTS` và `LECTURERS` giữ hồ sơ
riêng, mỗi hồ sơ gắn với đúng một tài khoản. `COURSE_SECTIONS` là bảng trung tâm —
nối môn học với học kỳ, giảng viên và phòng học. `REGISTRATIONS` nối sinh viên với lớp
học phần.

Ba bảng còn lại (`SUBJECTS`, `SEMESTERS`, `ROOMS`) là danh mục, không có liên kết với nhau.

Khi đọc tài liệu thiết kế, tên cột trong CSDL là `snake_case` (`student_code`) nhưng
tên trường trả về cho front-end là `camelCase` (`studentCode`). Bảng đối chiếu nằm ở
mục 3.2 của Quy ước API — đây là chỗ dễ sai nhất khi code, nên đọc lại trước khi map entity.
