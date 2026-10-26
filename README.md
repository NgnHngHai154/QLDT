# QLDT | Quản lý & Đăng ký Học phần Trực tuyến

Bài tập lớn IT3180 của Nhóm 20, Trường CNTT&TT, Đại học Bách khoa Hà Nội.

## Frontend

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

## Chuẩn bị sau khi clone

Tạo file cấu hình ở thư mục gốc trước khi chạy Compose hoặc backend:

```powershell
Copy-Item .env.example .env
```

Thay các giá trị mẫu trong `.env`, đặc biệt là mật khẩu MySQL và `JWT_SECRET`. Tạo virtual
environment và cài dependency backend (dùng `requirements-dev.txt` nếu cần chạy test):

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Nếu cần chạy test, dùng thay thế: pip install -r requirements-dev.txt
```

| Key | Mô tả |
|---|---|
| `MYSQL_DATABASE` | Tên database; mặc định `qldt`. |
| `MYSQL_USER` | Tài khoản MySQL cho ứng dụng; mặc định `app`. |
| `MYSQL_PASSWORD` | Mật khẩu tài khoản ứng dụng; bắt buộc, cần thay giá trị mẫu. |
| `MYSQL_ROOT_PASSWORD` | Mật khẩu root MySQL; bắt buộc, cần thay giá trị mẫu. |
| `JWT_SECRET` | Bí mật ký JWT; bắt buộc và tối thiểu 32 ký tự. |
| `MIN_CREDITS_PER_SEMESTER` | Số tín chỉ tối thiểu; mặc định tạm thời `12`. |
| `MAX_CREDITS_PER_SEMESTER` | Số tín chỉ tối đa; mặc định tạm thời `24`, phải >= 1 và >= mức tối thiểu. |

## Backend API

Yêu cầu Python 3.12 trở lên và MySQL 8.0.16 trở lên. Từ thư mục gốc, khởi động MySQL:

```powershell
docker compose up -d db
```

Sau đó cài và khởi động API:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload
```

API docs: `http://localhost:8000/api/docs`; health: `http://localhost:8000/health`.
Backend đọc cấu hình từ biến môi trường và file `.env` ở thư mục gốc; không dùng giá trị mẫu ở production.
Kiểm thử bằng `pytest` và `ruff check .` từ thư mục `backend/`.

Service đăng ký/hủy đã có luồng nghiệp vụ cơ bản; một số service catalog và timetable vẫn trả
`501 NOT_IMPLEMENTED`. Xem trạng thái chi tiết tại [backend/README.md](backend/README.md) và [tasks/BOARD.md](tasks/BOARD.md).

## Toàn bộ stack Docker

Từ thư mục gốc:

```powershell
docker compose up -d --build db
docker compose run --rm backend alembic upgrade head
docker compose run --rm backend python -m scripts.seed
docker compose up -d --build backend gateway
```

Gateway: `http://localhost:8080`; Swagger UI: `http://localhost:8080/api/docs`.
Deployment production và các secret được mô tả trong [docker-compose.prod.yml](docker-compose.prod.yml)
và workflow [CI/CD](.github/workflows/ci-cd.yml). Deploy qua SSH được tắt mặc định.

## Cấu trúc repository

- [docs/00-INDEX.md](docs/00-INDEX.md): bản đồ và nguồn tài liệu dự án.
- `contracts/`: hợp đồng API; `contracts/openapi.yaml` chưa được cung cấp.
- `backend/`: FastAPI, SQLAlchemy, Alembic, tests và seed tiện ích dev.
- `frontend/`: React + TypeScript + Vite.
- `db/`: SQL schema và seed chuẩn; tên database `qldt`.
- `gateway/`: reverse proxy Nginx và smoke test.
- `docker-compose.yml`, `docker-compose.prod.yml`: cấu hình local và production.
- `.github/workflows/ci-cd.yml`: lint, tests, migration checks, container integration, image publish; deployment SSH tùy chọn.
- `e2e/`, `tasks/`, `scripts/`: vùng test/workflow và theo dõi công việc.

## Trạng thái

Tiến độ, phần còn thiếu và trạng thái kiểm thử được theo dõi tại [tasks/BOARD.md](tasks/BOARD.md).
