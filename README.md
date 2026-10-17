# QLDT | Quản lý & Đăng ký Học phần Trực tuyến

Đồ án IT3180 của Nhóm 20, Trường CNTT&TT, Đại học Bách khoa Hà Nội.

## Bắt đầu với frontend

Yêu cầu Node.js 20 trở lên và npm.

```bash
cd frontend
npm install
npm run dev
```

Mở URL Vite hiển thị trong terminal. Kiểm tra production build bằng `npm run build`.

Tạo `frontend/.env.local` nếu cần đổi API origin:

```dotenv
VITE_API_BASE_URL=/api
```

Auth endpoint hiện dùng `POST /api/auth/login` và response `accessToken`; xác nhận field chi tiết với `contracts/openapi.yaml` trước khi tích hợp. Không dùng tài khoản demo giả trong UI.

## Chạy backend Sanic

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pip install -e .
$env:JWT_SECRET_KEY = (python -c "import secrets; print(secrets.token_urlsafe(48))")
$env:DB_HOST = "localhost"
$env:DB_NAME = "qldt"
$env:DB_USER = "root"
$env:DB_PASSWORD = "<local-password>"
python run.py
```

Use the single seeded admin account `admin` / `admin` for local auth checks; change it outside development. Lecturer and student sample accounts use `123456`.

## Bản đồ repository

- `docs/00-INDEX.md`: nơi bắt đầu và bản đồ tài liệu.
- `contracts/`: hợp đồng API; OpenAPI cần được bổ sung bởi nhóm backend.
- `frontend/`: ứng dụng React + TypeScript + Vite.
- `backend/`: Sanic API with `src/qldt/{auth,security,common}` in place; other business packages are ready for implementation.
- `db/`, `e2e/`, `tasks/`, `scripts/`: project data and member work areas.
- `db/`: schema, seed và vùng migrations dành cho thành viên DB.

## Trạng thái

Frontend có shell theo role, đăng nhập, đăng ký/hủy lớp, thời khóa biểu tuần và các trang tra cứu theo role. Build đã qua; luồng chính được smoke-test với mock trên browser. CRUD, chi tiết roster và API thật còn chờ `contracts/openapi.yaml`. Xem `tasks/BOARD.md`.
