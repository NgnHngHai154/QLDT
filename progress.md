# Tien do frontend QLDT

## Trang thai

**Auth backend đã chuyển sang Sanic trong `backend/src/qldt`; FE build và backend auth tests đều qua. Commit: `61d4900`.**

## Da kiem tra

- Frontend scaffold: React + TypeScript + Vite, Ant Design, React Router, Axios, TanStack Query.
- Login FE dùng `accessToken`, nested `user`, `GET /api/auth/me`; route guard theo role, bearer header, 401 xóa session và 403 giữ session.
- UC005: catalog hoc ky/lop, filter tren trang hien tai, badge `remainingSeats`/`full`/`registeredByMe`, confirm dang ky, POST `{sectionId}`, error mapping va refetch.
- UC006: danh sach dang ky va confirm huy qua `DELETE /registrations/{id}`, refetch sau ghi. Doi lop atomic chua co endpoint/UX da chot.
- UC007/UC008: luoi tuan theo `date`, `dayOfWeek`, tiet 1-12; chon hoc ky/tuan; student va lecturer dung `/me/timetable` tuong ung.
- UC002: ADMIN tra cuu subject/section; CRUD write chua bat do OpenAPI chua co schema ghi.
- UC003/UC009: endpoint roster duoc goi va dem so item; chua hien thi chi tiet sinh vien vi chua co roster field schema.
- Schema 8 bảng giữ tại `db/schema.sql`; seed mới một-admin được chuyển thành `db/seed/seed.sql`, registrations rỗng.
- Auth chuyển từ Flask demo ở root sang Sanic package `backend/src/qldt/{auth,security,common}`; chỉ có user repository MySQL, không có production mock fallback.
- Backend phát hành `POST /api/auth/login`, `GET /api/auth/me`, JWT access-only 3600s, RBAC decorator, camelCase user JSON và error envelope FE-BE.
- Đã bỏ Flask demo, refresh-token implementation và Java backend placeholders; PDFs nguồn đã chuyển vào `docs/source/`.
- Da tao `docs/` voi SRS UC001-UC009, NFR, API conventions, business rules, error mapping, naming-map tam, traceability va open questions tu tom tat duoc cung cap.
- Da cai dependencies bang Node.js 22.17.1 portable trong `%TEMP%`; `npm run build` thanh cong (TypeScript + Vite).
- Dev server dang chay tai `http://127.0.0.1:5173/`. Browser xac nhan login render tren viewport 390x844 khong tran ngang; UC005/UC006 mock smoke passed; thoi khoa bieu render tren 390px; guard role chan route sai va giu token. Test login/API that chua chay.
- Hien font dung stack local de tranh loi tai Google Fonts trong sandbox. Build co warning chunk Ant Design lon hon 500 kB; compressed entry khoang 260 kB, can toi uu neu team can NFR tai nang nhanh hon.
- `contracts/openapi.yaml` chua duoc cung cap; chua the verify payload voi backend, tao contract-generated mocks, hoan tat ADMIN CRUD, hoac hien roster detail fields.
- Backend tests dùng hash admin thật từ seed và fake repository trong test only; 7 test qua. Chưa kiểm tra kết nối MySQL thật.
- `backend/.env.example` không chứa secret; `JWT_SECRET_KEY` phải do môi trường local cung cấp, tối thiểu 32 bytes.
- Browser smoke tests dung route mocks tam thoi, chua duoc dong goi thanh Playwright tests trong repo. NFR response <2 giay chua do voi backend that.

## Ke hoach

Ke hoach chi tiet theo dung 10 muc yeu cau nam tai `docs/frontend-plan.md`.

## Dieu kien de bat dau

- Dua `openapi.yaml` vao workspace de sinh type/mock va chot schema request/response chi tiet.

## Viec tiep theo

- [x] Ghi lai luong, API/error contract va rang buoc nghiep vu tu ban tom tat nguoi dung cung cap.
- [x] Lap ke hoach 10 muc, sitemap, wireframe, kien truc, sprint, test va cau hoi mo.
- [ ] Bổ sung `contracts/openapi.yaml` và đối chiếu success/error schemas.
- [x] Tao app shell va slice login dau tien.
- [x] Cai dependencies, build va mo dev server bang Node portable.
- [x] Kiem tra login UI tren desktop va mobile viewport.
- [x] Tao module catalog, registration, timetable va noi role routes.
- [x] Tổ chức Python/Sanic backend auth và chuyển seed mới vào `db/`.
- [x] Chạy 7 backend auth tests; xác nhận seed có duy nhất admin và hash khớp password `admin`.
- [x] Commit thay đổi: `61d4900` (`feat: migrate auth module to Sanic and align database layout`).
- [ ] Doi chieu login, list, roster, registration, timetable schemas voi `contracts/openapi.yaml`.
- [ ] Chạy auth với MySQL thật và cấu hình secret qua environment.
- [ ] Hoan thien CRUD UI theo OpenAPI va hien thi day du roster field khi schema co.
