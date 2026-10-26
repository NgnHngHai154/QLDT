from datetime import date

from app.entity import Room, Semester, Subject
from tests.conftest import login


def _seed_basic_catalog(db_session):
    semester = Semester(
        semester_code="2026.1",
        name="Học kỳ 1 2026-2027",
        start_date=date(2026, 9, 7),
        end_date=date(2026, 12, 20),
        num_weeks=15,
    )
    room = Room(room_code="D9-301", building="D9", capacity=60)
    subject = Subject(subject_code="IT3180", name="Công nghệ phần mềm", credits=3)
    db_session.add_all([semester, room, subject])
    db_session.commit()
    return semester, room, subject


def test_uc002_manage_subjects(client, db_session):
    admin_headers = login(client, "admin", "Admin@123")

    # Tạo môn học mới
    create_res = client.post(
        "/api/subjects",
        json={"subjectCode": "IT3080", "name": "Mạng máy tính", "credits": 3},
        headers=admin_headers,
    )
    assert create_res.status_code == 201
    created_id = create_res.json()["id"]

    # Thử tạo trùng mã -> 409
    dup_res = client.post(
        "/api/subjects",
        json={"subjectCode": "IT3080", "name": "Mạng máy tính trùng", "credits": 3},
        headers=admin_headers,
    )
    assert dup_res.status_code == 409
    assert dup_res.json()["error"] == "DUPLICATE_CODE"

    # Lấy danh sách môn học
    list_res = client.get("/api/subjects", headers=admin_headers)
    assert list_res.status_code == 200
    assert any(item["subjectCode"] == "IT3080" for item in list_res.json()["items"])

    # Cập nhật môn học
    update_res = client.put(
        f"/api/subjects/{created_id}",
        json={"name": "Mạng máy tính nâng cao", "credits": 4},
        headers=admin_headers,
    )
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "Mạng máy tính nâng cao"


def test_uc002_manage_sections_and_conflicts(client, db_session):
    admin_headers = login(client, "admin", "Admin@123")
    semester, room, subject = _seed_basic_catalog(db_session)

    # Tạo lớp học phần thứ nhất
    section1_payload = {
        "sectionCode": "150001",
        "subjectId": subject.id,
        "semesterId": semester.id,
        "lecturerId": 1,
        "roomId": room.id,
        "dayOfWeek": 2,
        "startPeriod": 1,
        "endPeriod": 3,
        "startWeek": 1,
        "endWeek": 15,
        "maxCapacity": 50,
    }
    res1 = client.post("/api/sections", json=section1_payload, headers=admin_headers)
    assert res1.status_code == 201

    # Tạo lớp thứ 2 trùng phòng và trùng giờ -> 409 SCHEDULE_CONFLICT
    section2_payload = {
        "sectionCode": "150002",
        "subjectId": subject.id,
        "semesterId": semester.id,
        "lecturerId": 1,
        "roomId": room.id,
        "dayOfWeek": 2,
        "startPeriod": 2,
        "endPeriod": 4,
        "startWeek": 5,
        "endWeek": 10,
        "maxCapacity": 50,
    }
    res2 = client.post("/api/sections", json=section2_payload, headers=admin_headers)
    assert res2.status_code == 409
    assert res2.json()["error"] == "SCHEDULE_CONFLICT"


def test_uc005_uc006_student_registration_and_cancel(client, db_session):
    admin_headers = login(client, "admin", "Admin@123")
    student_headers = login(client, "sv1", "Sv@12345")
    semester, room, subject = _seed_basic_catalog(db_session)

    # Admin mở lớp
    sec_payload = {
        "sectionCode": "150005",
        "subjectId": subject.id,
        "semesterId": semester.id,
        "lecturerId": 1,
        "roomId": room.id,
        "dayOfWeek": 3,
        "startPeriod": 1,
        "endPeriod": 3,
        "startWeek": 1,
        "endWeek": 15,
        "maxCapacity": 1,  # chỉ chứa 1 sinh viên để test full
    }
    sec_res = client.post("/api/sections", json=sec_payload, headers=admin_headers)
    assert sec_res.status_code == 201
    sec_id = sec_res.json()["id"]

    # UC005: Sinh viên đăng ký
    reg_res = client.post("/api/registrations", json={"sectionId": sec_id}, headers=student_headers)
    assert reg_res.status_code == 201
    reg_id = reg_res.json()["id"]
    assert reg_res.json()["section"]["registeredByMe"] is True

    # Thử đăng ký lại -> 409 ALREADY_REGISTERED
    dup_reg = client.post("/api/registrations", json={"sectionId": sec_id}, headers=student_headers)
    assert dup_reg.status_code == 409
    assert dup_reg.json()["error"] == "ALREADY_REGISTERED"

    # Xem danh sách lớp đã đăng ký
    my_regs = client.get(
        "/api/registrations/me", params={"semesterId": semester.id}, headers=student_headers
    )
    assert my_regs.status_code == 200
    assert len(my_regs.json()["items"]) == 1

    # UC007: Xem thời khóa biểu sinh viên
    timetable_res = client.get(
        "/api/students/me/timetable",
        params={"semesterId": semester.id, "week": 2},
        headers=student_headers,
    )
    assert timetable_res.status_code == 200
    assert len(timetable_res.json()["items"]) == 1
    assert timetable_res.json()["items"][0]["sectionCode"] == "150005"

    # UC003 / UC009: Admin và Giảng viên xem danh sách sinh viên lớp này
    gv_headers = login(client, "gv1", "Gv@12345")
    roster_res = client.get(f"/api/sections/{sec_id}/students", headers=gv_headers)
    assert roster_res.status_code == 200
    assert roster_res.json()["currentEnrollment"] == 1
    assert roster_res.json()["items"][0]["studentCode"] == "20210001"

    # UC008: Giảng viên xem lịch dạy & lớp phụ trách
    lec_timetable = client.get(
        "/api/lecturers/me/timetable",
        params={"semesterId": semester.id, "week": 2},
        headers=gv_headers,
    )
    assert lec_timetable.status_code == 200
    assert len(lec_timetable.json()["items"]) == 1

    lec_sections = client.get(
        "/api/lecturers/me/sections",
        params={"semesterId": semester.id},
        headers=gv_headers,
    )
    assert lec_sections.status_code == 200
    assert len(lec_sections.json()["items"]) == 1

    # UC006: Hủy đăng ký
    del_res = client.delete(f"/api/registrations/{reg_id}", headers=student_headers)
    assert del_res.status_code == 204

    # Kiểm tra lại danh sách lớp sau khi hủy
    after_cancel = client.get(
        "/api/registrations/me", params={"semesterId": semester.id}, headers=student_headers
    )
    assert len(after_cancel.json()["items"]) == 0
