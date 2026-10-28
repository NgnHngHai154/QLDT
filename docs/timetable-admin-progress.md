# Tiến độ giao diện xếp lịch và phân công

## Phạm vi

Màn hình quản trị lịch học nằm tại `/app/timetable/manage` trong vùng yêu cầu quyền Admin, gồm danh sách lớp học phần và form điều chỉnh giảng viên, phòng, thứ, tiết và tuần học. Đường dẫn cũ `/timetable/manage` chuyển hướng vào vùng bảo vệ này.

## Quy tắc nghiệp vụ

Quyen quan tri chi duoc truy cap tai `/app/timetable/manage`; duong dan cu `/timetable/manage` redirect vao khu vuc duoc bao ve.

- Giao diện gửi thay đổi lên `PUT /api/sections/{id}`; backend xác thực tiết/tuần, sức chứa và xung đột lịch trước khi commit.
- Lỗi `SCHEDULE_CONFLICT` và các lỗi validation được hiển thị từ response backend; giao diện không lưu lịch giả trong bộ nhớ.
- Lớp đã có đăng ký không cho đổi môn hoặc học kỳ; các ràng buộc còn lại do service backend quyết định.

## Trạng thái tích hợp

- Danh sách và lookup được tải từ `/api/sections`, `/api/sections/lookups` và `/api/semesters/current`.
- Sau khi lưu thành công, React Query tải lại dữ liệu để giữ giao diện nhất quán với DB.
- Đã xác nhận frontend build thành công bằng `npm --prefix frontend run build`.
