# Ke hoach thiet ke Front-end QLDT

Pham vi: lap ke hoach, chua trien khai code. Can duyet stack, thoi luong va cac diem mo o muc 10 truoc khi scaffold.

## 1. Nguoi dung va luong chinh

| Vai tro | Nhu cau | Use case |
|---|---|---|
| ADMIN | Quan ly mon/lop; xem danh sach sinh vien cua lop | UC002, UC003 |
| LECTURER | Xem lich day theo hoc ky/tuan; xem danh sach sinh vien lop minh phu trach | UC008, UC009 |
| STUDENT | Dang ky, huy/doi lop; xem thoi khoa bieu theo hoc ky/tuan | UC005, UC006, UC007 |
| Ca ba | Dang nhap va vao dung khu vuc theo role | UC001 |

**Dang nhap:** mo `/login` -> nhap thong tin theo schema `POST /api/auth/login` -> luu token -> lay user qua `GET /api/auth/me` neu response login chua du thong tin -> dieu huong theo `user.role`. Sai thong tin hien loi tai form; `ACCOUNT_LOCKED` hien trang thai tai khoan. Khong co dang ky tai khoan.

**Dang ky lop:** STUDENT chon hoc ky -> tai danh sach tu `GET /api/sections?semesterId=...` -> loc/tim tren danh sach phan trang -> xem lich va si so -> chi bat nut khi `full` la false va `registeredByMe` la false -> `POST /api/registrations` voi `sectionId` -> tai lai danh sach va `GET /api/registrations/me?semesterId=...`. Server quyet dinh ket qua cuoi cung; UI xu ly cac loi 409 va khong tu sua si so.

**Huy/doi lop:** xem dang ky cua minh -> xac nhan huy -> `DELETE /api/registrations/{id}` -> tai lai du lieu. Doi lop hien chua co endpoint doi lop/nghiep vu atomic; tam thoi khong thiet ke nhu mot giao dich dam bao thanh cong ca hai buoc. Can nhom xac nhan UX doi lop la huy roi dang ky lai hay bo ngo.

**Them lop hoc phan:** ADMIN mo danh sach lop -> tao moi -> tai lookup tu `GET /api/sections/lookups` -> dien form va gui theo schema CRUD trong OpenAPI -> gan loi `VALIDATION_ERROR` vao field -> xu ly `SCHEDULE_CONFLICT` bang thong bao va chi tiet duoc backend tra ve -> refresh danh sach.

**Xem thoi khoa bieu tuan:** chon hoc ky -> lay `currentWeek` tu `GET /api/semesters/current` lam mac dinh -> tai `GET /api/students/me/timetable?semesterId=...&week=...` hoac endpoint lecturer tuong ung -> ve cot ngay/thu, hang tiet 1-12, card theo `date`, `dayOfWeek`, `startPeriod`, `endPeriod` -> chuyen tuan va tai lai. Chua quy doi tiet sang gio dong ho.

## 2. Sitemap va routing

> Cac duong dan duoi day la route frontend de xuat, khong phai API. Ten API giu dung hop dong; vai tro route lay tu `user.role`.

| FE route | Role | UC | API chinh |
|---|---|---|---|
| `/login` | Chua dang nhap | UC001 | `POST /api/auth/login`, `GET /api/auth/me` |
| `/student/sections` | STUDENT | UC005 | `GET /api/semesters`, `GET /api/sections?semesterId=...`, `POST /api/registrations` |
| `/student/registrations` | STUDENT | UC006 | `GET /api/registrations/me?semesterId=...`, `DELETE /api/registrations/{id}`, `POST /api/registrations` |
| `/student/timetable` | STUDENT | UC007 | `GET /api/semesters/current`, `GET /api/students/me/timetable` |
| `/lecturer/timetable` | LECTURER | UC008 | `GET /api/semesters/current`, `GET /api/lecturers/me/timetable`, `GET /api/lecturers/me/sections` |
| `/lecturer/sections/:sectionId/students` | LECTURER | UC009 | `GET /api/sections/{id}/students` |
| `/admin/subjects` | ADMIN | UC002 | `/api/subjects` CRUD |
| `/admin/sections` | ADMIN | UC002 | `/api/sections` CRUD, `GET /api/sections/lookups` |
| `/admin/sections/:sectionId/students` | ADMIN | UC003 | `GET /api/sections/{id}/students` |

Guard: khong co token -> `/login`; co token thi xac thuc user theo hop dong `/api/auth/me`; sai role -> trang 403/no-access, khong render menu route khong duoc cap quyen. 401 xoa token va ve login; 403 giu session va chi hien loi. Sau refresh, khoi phuc role tu API, khong tin role tu URL/client cache.

## 3. Man hinh va wireframe dang chu

Tat ca man hinh co loading, empty, error va success state tuong ung. Tren mobile, chuyen menu thanh drawer; bang co the scroll ngang hoac hien card theo hang; form xep mot cot; modal dung full-screen sheet neu khong du chieu rong.

| Man hinh | Bo cuc va thanh phan | Hanh vi/states mobile |
|---|---|---|
| Dang nhap | Logo/ten he thong; username, password; nut dang nhap; thong bao loi tai form | Form mot cot, submit bang ban phim; loading disable nut; khong co link dang ky |
| Dang ky lop | Chon hoc ky; tim/loc theo cac field duoc OpenAPI xac nhan; bang lop co phan trang; detail drawer; tab/danh sach lop da dang ky | Bo loc thanh panel thu gon; bang thanh card; nut dang ky ro rang; empty khi khong co lop |
| Dang ky cua toi | Hoc ky; danh sach lop da dang ky; action huy va doi lop (chi mo neu UX duoc duyet); modal xac nhan huy | Card lop; confirm sheet; pending state; tai lai sau ghi |
| Thoi khoa bieu sinh vien | Chon hoc ky/tuan; prev/next week; luoi ngay x tiet; lop hien trong block | Cho cuon ngang theo ngay; hien ro ngay va tiet; khong dung hover lam kenh thong tin duy nhat |
| Mon hoc ADMIN | Bang phan trang; tim kiem; tao/sua form; confirm xoa | Bang->card; form mot cot; empty state co action tao moi |
| Lop hoc phan ADMIN | Bang loc theo hoc ky; tao/sua form dung lookups; confirm xoa | Bo loc gon; form mot cot; neu conflict thi giu input va hien loi |
| Sinh vien trong lop | Tieu de lop va bang sinh vien theo response | Card hoac bang cuon ngang; khong expose lop ngoai pham vi role |
| Lich giang vien | Chon hoc ky/tuan; luoi lich day; danh sach lop phu trach | Cung quy tac lich responsive; cho mo danh sach sinh vien lop |
| 403/404 | Thong diep ngan, nut quay lai khu vuc hop le | Khong hien stack trace/path noi bo |

## 4. Design system de xuat

| Nhom | De xuat |
|---|---|
| Mau | Do HUST lam mau nhan dien (tam dung `#A6192E`, can nhom xac nhan mau/asset chinh thuc); nen trang/xam nhat; chu than; xanh la cho thanh cong/con cho, ho phach cho canh bao, do loi, xanh lam thong tin. Dam bao contrast AA. |
| Chu | `Be Vietnam Pro` neu duoc phep tai/nhung; fallback sans-serif co ho tro tieng Viet. Tieu de vua phai, bang va form uu tien do doc. |
| Spacing | He 4/8px; content desktop co max-width; mobile padding 16px; khoang cach nhat quan. |
| Components | AppShell, RoleNav, PageHeader, SemesterWeekSelector, PaginatedTable, SearchFilters, FormField, ErrorSummary, ConfirmDialog, Toast, EmptyState, LoadingSkeleton. |
| Lop hoc phan | Card/bang co badge con cho/day; nguon la `remainingSeats`/`full`; hien thi dang ky cua minh theo `registeredByMe`. Khong tu tinh toan so cho. |
| Lich | WeekGrid 7 ngay x tiet 1-12; card co ten lop va thong tin co trong response; card khong chong lan, co accessible label. Gio dong ho doi den khi co bang quy doi tiet. |

Muc tieu la giao dien tac vu hoc vu, scan duoc nhanh va nhat quan; lay cam hung tu nhan dien va phan nhom vai tro tren HUST, khong clone trang chu hay man hinh noi bo.

## 5. Kien truc ma nguon de xuat

```text
src/
  app/                 # router, providers, app shell
  api/
    client.ts          # Axios instance, /api base, bearer token
    errors.ts          # parse {status,error,message,details,path,timestamp}
    api-types.ts       # sinh tu openapi.yaml hoac type theo schema da xac nhan
  modules/
    auth/              # login, current user, role guard
    catalog/           # subjects, sections, lookups, class roster
    registration/      # danh sach lop, dang ky, huy/doi
    timetable/         # lich SV/GV, week grid
  shared/
    components/        # bang, form, modal, toast, state views
    hooks/
    utils/             # format ngay, mapping error
  styles/              # tokens, responsive rules
```

- **Stack:** React + TypeScript + Vite; React Router cho route theo role; Ant Design cho bang/form/modal; Axios theo yeu cau interceptor; TanStack Query de quan ly server state va invalidate/refetch sau mutation. Ly do: pho bien, co san component tac vu, chia module cho 5 nguoi va khong phai tu viet data cache.
- **Types:** uu tien sinh type tu `openapi.yaml` bang OpenAPI TypeScript; file nay chua co trong workspace. Truoc khi co, chi khai bao type cho payload da xac nhan, ghi ro schema con thieu; khong tu phat minh field.
- **State:** Query cache cho API; state local cho filter/form/modal. Khong can Redux/Zustand neu khong phat sinh nhu cau.
- **Token:** luu sessionStorage lam phuong an tam cho token 1 gio, xoa khi logout/401; khong luu password. Can nhom chap nhan rui ro XSS cua web storage va chinh sach CSP/sanitize; khong doi sang cookie vi chua co contract.
- **Axios:** gan `Authorization: Bearer <token>`; 401 xoa token, clear cache va redirect login mot lan; 403 giu token, hien loi; parse loi theo `error`, khong branching theo `message`.
- **Mock:** dung Prism/Postman tu `openapi.yaml` khi co schema. Hien repo chua co file nay, do do chua the tao mock contract day du.

## 6. Ba man hinh kho

### A. Dang ky hoc phan

1. Hoc ky bat buoc cho `GET /api/sections`; danh sach dung server pagination (`page`, `size`, `sort`) va envelope `{items: [...]}`.
2. Render cac field theo response schema. Su dung `remainingSeats`, `full`, `registeredByMe` de hien thi badge/disable nut. Khong tu tinh so cho va khong coi UI check la bao dam tranh race.
3. Gui `POST /api/registrations` voi `{sectionId}`. Trong luc gui, disable action cua dong do; khong optimistic update si so.
4. Thanh cong: invalidate/refetch danh sach lop va `GET /api/registrations/me?semesterId=...`.
5. 409: map loi; refetch danh sach de cap nhat trang thai, giu ngu canh loc/hoc ky. Loi `STUDENT_SCHEDULE_CONFLICT` co the dua toi lich cua toi neu co API data, khong tu suy tiet xung dot.

### B. Quan ly lop hoc phan

1. Load `GET /api/sections/lookups` va danh sach lop; lookup response fields phai doi chieu OpenAPI truoc khi lam form.
2. Form create/edit chi dung field va body theo OpenAPI; khoa ngoai ghi bang `xxxId`, object nested chi dung khi doc.
3. `VALIDATION_ERROR`: map `details[].field` vao field; cac loi khong gan duoc vao field hien trong ErrorSummary.
4. `SCHEDULE_CONFLICT`: hien thong bao tong quat va tung chi tiet neu response `details[]` co thong tin doc duoc; khong parse chuoi `message` thanh logic.
5. Xoa mon/lop can confirm; neu `SUBJECT_HAS_SECTIONS`/`SECTION_HAS_REGISTRATIONS`, giu du lieu va thong bao ly do. Sau ghi thanh cong refetch danh sach.

### C. Thoi khoa bieu tuan

1. Hien hoc ky va tuan hien tai tu `GET /api/semesters/current`; endpoint timetable nhan `semesterId`, `week`.
2. Luoi hien ngay theo `date`/`dayOfWeek`, tiet 1-12; block chiem cac hang `startPeriod` den `endPeriod` (xac nhan inclusive/exclusive tu contract).
3. Prev/next va chon tuan tai lai API; `INVALID_WEEK` hien thong bao, chuyen ve `currentWeek` hoac week hop le server tra ve neu co; khong tu doan gio hoc.
4. Student goi endpoint `/students/me/timetable`; lecturer goi `/lecturers/me/timetable`. Danh tinh lay tu token, client khong gui studentId/lecturerId.

## 7. Ma loi -> hanh vi UI

Tat ca loi hien thong diep tieng Viet than thien; khong dua stack trace/SQL/path noi bo ra UI. Nhanh theo `error`; `message` chi co the dung lam fallback da loc, khong lam dieu kien.

| `error` | Vi tri va hanh vi |
|---|---|
| `INVALID_CREDENTIALS` | Form login; bao thong tin dang nhap khong dung, khong tiet lo username co ton tai hay khong. |
| `ACCOUNT_LOCKED` | Form/login page; huong dan lien he quan tri, khong cho thu lai lien tuc. |
| `TOKEN_EXPIRED`, `UNAUTHORIZED` | 401: xoa token/cache va chuyen login; giu `redirectTo` noi bo neu duoc phe duyet. |
| `FORBIDDEN` | 403: toast/page khong quyen; giu token, khong logout. |
| `VALIDATION_ERROR` | Field error theo `details[].field`; phan con lai vao ErrorSummary. |
| `CLASS_FULL` | Toast/banner dang ky; refetch danh sach va cap nhat badge. |
| `ALREADY_REGISTERED` | Dong lop/action; refetch registrations, khong tao ban ghi client. |
| `SAME_SUBJECT_REGISTERED` | Dang ky; chi ra da co lop cung mon neu response cung cap du thong tin. |
| `STUDENT_SCHEDULE_CONFLICT` | Dang ky; thong bao trung lich va refetch; khong tu suy lop nao trung neu details khong neu. |
| `DUPLICATE_CODE` | Form mon/lop; gan vao field ma tu `details[].field` neu co, giu cac gia tri khac. |
| `SCHEDULE_CONFLICT` | Form lop; ErrorSummary va details backend tra ve. |
| `CAPACITY_BELOW_ENROLLMENT` | Field `maxCapacity` neu details chi ro; chan luu de nguoi dung sua. |
| `SECTION_HAS_REGISTRATIONS` | Confirm/delete action; bao khong the xoa lop dang co SV dang ky. |
| `SUBJECT_HAS_SECTIONS` | Confirm/delete action; bao khong the xoa mon da mo lop. |
| `INVALID_WEEK` | Week selector/timetable; thong bao va dua ve tuan hop le/currentWeek neu biet. |
| HTTP 404 | Trang/ban ghi khong con ton tai; co action quay lai va refetch danh sach. |
| HTTP 500 hoac loi khong nhan dien | Toast tong quat, khong hien ky thuat; cho thu lai. Ghi log an toan chi voi request id neu backend co tra. |

Status HTTP theo quy uoc: 400 validation, 401 auth, 403 role, 404 not found, 409 business conflict, 500 server. Khong suy status rieng cho tung ma loi neu OpenAPI chua gan.

## 8. Ke hoach sprint va chia viec

**Gia dinh lap ke hoach:** 4 sprint x 1 tuan (4 tuan), 5 thanh vien; FE lam song song BE. Can nhom doi chieu voi thoi gian thuc te. Moi thanh vien review chéo va cap nhat integration branch hang ngay.

| Sprint | Thanh vien / dau viec | Phu thuoc va demo |
|---|---|---|
| 1 - Nen tang | TV1: scaffold, shell, tokens, CI script. TV2: auth flow va route guard. TV3: OpenAPI/type map, subject API. TV4: section API/mock contract. TV5: registration/timetable API contract va test setup. | Can chot OpenAPI, stack, login schema, response shapes. Demo app shell, login mock, menu role; neu OpenAPI tre thi demo bang fixtures duoc danh dau. |
| 2 - Chuc nang cot loi | TV1: shared table/form/modal va integration. TV2: auth/error interceptor, access tests. TV3: ADMIN subjects CRUD. TV4: ADMIN sections CRUD/lookups/roster. TV5: STUDENT danh sach lop va dang ky/huy. | Sections/lookups va business errors phai co contract/mock. Demo CRUD mon/lop va dang ky co refetch. |
| 3 - Lich va hoan thien role | TV1: responsive/accessibility review. TV2: session expiry/403, regression. TV3: hoan thien catalog/validation. TV4: lecturer sections va danh sach SV. TV5: student/lecturer timetable, week navigation, registration edge cases. | Can chot shape timetable, `currentWeek`, lich detail va quy doi tiet neu can. Demo end-to-end cac role. |
| 4 - Tich hop/nghiem thu | Ca nhom: integration voi BE, Playwright flows, responsive, performance, fix bug; TV1 dieu phoi demo/tai lieu; moi owner sua module minh. | API deployed hoac mock giong OpenAPI. Demo UC001-009 trong pham vi; gate build/lint/tests va checklist duoi 2 giay. |

**Thu tu phu thuoc:** OpenAPI/contract -> API types/mock -> auth + app shell -> module features -> integrated flows -> E2E/performance. Cong viec TV3/4/5 co the song song sau khi API types va shared UI duoc chot.

**Rui ro/giam thieu:** OpenAPI den muon (mock Prism tu schema; khong tu tao schema); BE doi response (contract review hang ngay); concurrency full/conflict (server la nguon su that, refetch); token khong refresh (xu ly 401 dung, canh bao thao tac dang do); thieu bang tiet-gio (hien tiet so); mobile timetable rong (cuon ngang va test thiet bi); 4 tuan qua ngan (uu tien UC001, UC005-008, sau do UC002/003/009 theo rubric).

## 9. Kiem thu front-end

- **Unit:** format ngay/timezone +07:00; mapping `error`; guard role; layout tiet/thu; serialize query page/size/sort; khong test logic server-side nhu race capacity.
- **Component:** login validation/loading; pagination envelope `{items}`; nut dang ky theo `full`/`registeredByMe`; field error theo `details[].field`; confirm huy/xoa; timetable loading/empty/error/INVALID_WEEK.
- **Contract:** request `POST /registrations` chi co `sectionId`; authorization header; path/query dung endpoint; JSON camelCase/null; enum UPPER_SNAKE_CASE. Dung Prism khi co `openapi.yaml`.
- **E2E:** login moi role; role sai bi chan; student dang ky thanh cong/refetch; server tra tung loi 409; huy dang ky; admin CRUD va constraint errors; lecturer chi xem lop cua minh; doi tuan cho ca student/lecturer.
- **Responsive:** desktop/tablet/mobile; menu drawer; bang khong lam tran viewport; timetable co cuon ngang co chu thich; form/modal khong bi cat; focus/keyboard/contrast.
- **Hieu nang:** lay moc tuong tac tra cuu/gui form <2s trong moi truong demo da thong nhat; phan biet thoi gian FE va API; server pagination, tranh goi lai trung lap, lazy-load route neu bundle lon. NFR can chot cach do, thiet bi va p95/p90.

## 10. Cau hoi mo va gia dinh

| Cau hoi | Gia dinh tam thoi / tac dong |
|---|---|
| Stack/UI library va browser muc tieu? | De xuat React+TS+Vite, Ant Design; can nhom duyet truoc scaffold. |
| Sprint dai bao lau? | Ke hoach tam 4 sprint x 1 tuan; can chot ngay demo/rubric. |
| `openapi.yaml` o dau, schema co day du endpoint/error khong? | La nguon chuan cuoi; can dua vao repo de sinh type/mock va xac nhan request/response. |
| Login request/response, `/auth/me`, token expiry va logout optional? | Chua co schema field; khong tu dat username/password key hoac xu ly logout server truoc khi doc OpenAPI. |
| `GET /sections/lookups`, subject/section, registrations va timetable tra field gi? | Chi dung field da neu; can schema day du truoc khi viet form/table/grid. |
| `details[]` co shape gi ngoai `field`? `SCHEDULE_CONFLICT` tra chi tiet nao? | Hien thong bao tong quat cho den khi co schema. |
| Doi lop la huy roi dang ky lai hay can thao tac atomic? | Hien chua co API doi lop; khong cam ket atomic va can nhom quyet dinh. |
| Bang quy doi tiet 1-12 sang gio, gio nghi/ca hoc? | Hien thi tiet so; chua ve theo gio dong ho. |
| `startPeriod`/`endPeriod` inclusive? `date`/`dayOfWeek` can doi chieu ra sao? | Dung dung response de ve; can xac nhan boundary va timezone. |
| Mau/logo/font HUST co duoc phep su dung? | Chi lay cam hung phan cap/navi; mau #A6192E la mau tam, can xac nhan nhan dien. |
| 2 giay do tren may/mang nao, tinh API hay chi frontend? | Do rieng thoi gian FE va API tren moi truong demo; can chot nguong percentile. |
| Co can phan trang danh sach sinh vien khong? | Khong tu them query; neu API khong phan trang thi can xac nhan gioi han du lieu. |

**Nguon contract:** quy uoc API FE-BE cap nhat uu tien hon mo ta cu trong thiet ke; `openapi.yaml` la nguon chuan cuoi theo thong tin duoc cung cap. Neu thieu/khac nhau, dung va xin xac nhan thay vi tu dien.