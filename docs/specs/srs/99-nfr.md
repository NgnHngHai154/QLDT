# 99. Yêu cầu phi chức năng

| ID | Yêu cầu |
|---|---|
| NFR-001 | Mật khẩu được băm Bcrypt; không trả hash qua API. |
| NFR-002 | JWT và RBAC; token hết hạn sau 3600 giây, không có refresh token. |
| NFR-003 | Giao diện responsive cho desktop và mobile. |
| NFR-004 | REST API, client/server tách biệt. |
| NFR-005 | Tra cứu và gửi form phản hồi dưới 2 giây; cần chốt môi trường/cách đo. |
| NFR-006 | Toàn vẹn dữ liệu bằng PK, FK, UNIQUE, CHECK. |

Thông báo UI không làm lộ chi tiết kỹ thuật. Frontend dùng phân trang server-side cho môn/lớp và tránh yêu cầu lặp; không thể đảm bảo end-to-end <2 giây nếu API/backend vượt ngân sách.