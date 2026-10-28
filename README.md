# QLDT — Quản lý và đăng ký học phần

Dự án môn IT3180, Nhóm 20. Stack: React + TypeScript, FastAPI, MySQL.

## Chạy FE–BE–DB local (Windows)

Yêu cầu Docker Desktop, Python 3.12+, Node.js 20+ và npm. Tại thư mục gốc, tạo cấu hình một lần:

```powershell
Copy-Item .env.example .env
```

Thay `MYSQL_PASSWORD`, `MYSQL_ROOT_PASSWORD` và `JWT_SECRET` trong `.env` (JWT tối thiểu 32 ký tự). Chạy MySQL:

```powershell
docker compose up -d db
```

Mở terminal thứ hai để chạy backend:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload
```

Mở terminal thứ ba để chạy frontend:

```powershell
cd frontend
npm install
npm run dev
```

Vite chạy tại `http://localhost:5173`, proxy `/api` tới backend `http://localhost:8000`. API docs: `http://localhost:8000/api/docs`; health: `http://localhost:8000/health`.

Seed dev tạo tài khoản `admin / admin`, `gv001 / 123456`, `sv20210001 / 123456`. Chỉ dùng các mật khẩu mẫu ở môi trường local.

### Nạp bộ dữ liệu đầy đủ (100 môn học / 400 lớp)

`python -m scripts.seed` chỉ tạo dữ liệu dev tối thiểu. Để dùng bộ dữ liệu chuẩn trong
`db/seed/seed.sql` (1.000 sinh viên, 10 giảng viên, 100 môn, 400 lớp), thay toàn bộ schema và
dữ liệu hiện tại của database `qldt`:

> Cảnh báo: `db/schema.sql` xóa và tạo lại toàn bộ bảng. Sao lưu dữ liệu cần giữ trước khi chạy.
> Trên database mới, dùng cách này **thay cho** `alembic upgrade head` + `python -m scripts.seed`
> (xem [db/README.md](db/README.md)); không áp dụng cả hai lên cùng một database.

```powershell
docker compose exec -T db sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysqldump -uroot --databases qldt > /tmp/qldt-backup.sql'
docker compose cp db:/tmp/qldt-backup.sql qldt-backup.sql
docker compose cp db/schema.sql db:/tmp/schema.sql
docker compose cp db/seed/seed.sql db:/tmp/seed.sql
docker compose exec -T db sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -uroot < /tmp/schema.sql'
docker compose exec -T db sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql -uroot qldt < /tmp/seed.sql'
```

Sau đó khởi động lại backend và tải lại frontend. Dữ liệu nằm trong Docker volume `dbdata`,
nên chỉ cần nạp **một lần**; không cần chạy lại mỗi lần khởi động máy. Chỉ nạp lại khi muốn reset
database hoặc sau khi xóa volume bằng `docker compose down -v`.

## Chạy kiểm tra

```powershell
# backend (trong backend/ và đã activate .venv)
ruff check .
pytest

# frontend (trong frontend/)
npm run build
```

## Kiểm thử quản trị đào tạo (Feature 10)

Sau khi chạy migration và `python -m scripts.seed`, nạp bộ dữ liệu thử nghiệm:

```powershell
cd backend
python -m scripts.seed_test_data
pytest
pytest -m integration
```

`pytest -m integration` cần MySQL, gateway và frontend đang chạy; xem hướng dẫn đầy đủ,
bảng dữ liệu và checklist giao diện tại [docs/testing/feature10-admin-training.md](docs/testing/feature10-admin-training.md).

## Nguồn dữ liệu và hợp đồng

- `db/schema.sql` và `db/seed/seed.sql` là schema/seed SQL chuẩn; xem [db/README.md](db/README.md). Không nạp SQL seed lên database đã có dữ liệu nếu chưa xác nhận tác động.
- Hợp đồng FE–BE nằm tại `contracts/openapi.yaml` và `contracts/api-types.ts`. JSON dùng camelCase; object môn/lớp/học kỳ trả `id`, còn request tham chiếu dùng `subjectId`, `sectionId`, `semesterId`.
- Backend theo luồng `controller → service → repository → entity`; nghiệp vụ đăng ký, xung đột và sĩ số do server quản lý.
- [backend/README.md](backend/README.md) và [frontend/README.md](frontend/README.md) có ghi chú riêng cho từng ứng dụng.
