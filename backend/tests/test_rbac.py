"""Kiểm tra lớp phân quyền thứ nhất (Security Filter)."""

from tests.conftest import login


def test_public_course_catalog_is_readable_without_login(client):
    res = client.get("/api/subjects")
    assert res.status_code == 200
    assert "items" in res.json()


def test_student_can_read_course_catalog(client):
    res = client.get("/api/subjects", headers=login(client, "sv1", "Sv@12345"))
    assert res.status_code == 200
    assert "items" in res.json()


def test_lecturer_cannot_register(client):
    res = client.post(
        "/api/registrations", json={"sectionId": 1}, headers=login(client, "gv1", "Gv@12345")
    )
    assert res.status_code == 403


def test_admin_passes_filter_and_reaches_service(client):
    res = client.get("/api/subjects", headers=login(client, "admin", "Admin@123"))
    assert res.status_code == 200
    assert "items" in res.json()


def test_section_payload_validation_points_at_field(client):
    payload = {
        "sectionCode": "150001",
        "subjectId": 1,
        "semesterId": 1,
        "lecturerId": 1,
        "roomId": 1,
        "dayOfWeek": 3,
        "startPeriod": 5,
        "endPeriod": 3,
        "startWeek": 1,
        "endWeek": 15,
        "maxCapacity": 0,
    }
    res = client.post("/api/sections", json=payload, headers=login(client, "admin", "Admin@123"))
    assert res.status_code == 400
    fields = {d["field"] for d in res.json()["details"]}
    assert {"endPeriod", "maxCapacity"} <= fields
