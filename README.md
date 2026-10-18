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
Copy-Item .env.example .env
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload
```

API docs: `http://localhost:8000/api/docs`; health: `http://localhost:8000/health`.
Chỉnh `backend/.env` để thay `DATABASE_URL` và `JWT_SECRET`; không dùng secret mặc định ở production.
Kiểm thử bằng `pytest` và `ruff check .` từ thư mục `backend/`.

Một số service catalog, registration và timetable vẫn là khung trả `501 NOT_IMPLEMENTED`;
xem trạng thái chi tiết tại [backend/README.md](backend/README.md) và [tasks/BOARD.md](tasks/BOARD.md).

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
