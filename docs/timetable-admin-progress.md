# Tiến độ giao diện xếp lịch và phân công

## Phạm vi

Đã bổ sung màn hình tại \`/timetable/manage\` (public, không yêu cầu đăng nhập) và \`/app/timetable/manage\` (menu Admin), gồm danh sách lớp học phần và form điều chỉnh giảng viên, phòng, thứ, tiết và tuần học.

## Quy tắc nghiệp vụ được áp dụng ở giao diện

- Không cho lưu nếu tiết bắt đầu lớn hơn tiết kết thúc hoặc nằm ngoài khoảng 1-12.
- Không cho trùng phòng hoặc trùng giảng viên khi cùng ngày, cùng khoảng tiết và cùng tuần học.
- Hiển thị trạng thái xung đột riêng cho giảng viên và phòng trước khi lưu.

## Trạng thái tích hợp

- Dữ liệu hiện là mock trong bộ nhớ trình duyệt để phục vụ kiểm thử giao diện.
- Backend timetable hiện vẫn trả 501 theo BOARD; cần hoàn thiện API/OpenAPI trước khi nối thao tác lưu thật.
- Đã xác nhận frontend build thành công bằng \`npm --prefix frontend run build\`.
