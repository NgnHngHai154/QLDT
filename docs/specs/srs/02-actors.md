# 02. Tác nhân và Use Case

| Actor | Nhu cầu/use case |
|---|---|
| ADMIN | UC002 quản lý môn học/lớp học phần; UC003 xem sinh viên đăng ký theo lớp |
| LECTURER | UC008 xem lịch dạy theo học kỳ/tuần; UC009 xem sinh viên lớp mình phụ trách |
| STUDENT | UC005 đăng ký lớp; UC006 hủy/đổi lớp; UC007 xem thời khóa biểu |
| Tất cả | UC001 đăng nhập và phân quyền |

UC004 xác thực phiên và kiểm tra quyền sinh viên được UC005, UC006, UC007 include. UC002.9 kiểm tra xung đột phòng/giảng viên khi thêm hoặc sửa lớp.