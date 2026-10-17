# file đung để test auth.py mà không cần MySQL, khong phải nội dung chính, có thể bỏ qua nếu muốn. Chỉ cần chạy `python test_auth.py` là được.
"""
=======================================================================
test_auth.py  -  Test tu dong cho auth.py (khong can MySQL)
=======================================================================
Chay:  python test_auth.py
=======================================================================
"""

import sys
import os
import json
import unittest
import io

# Fix Windows console encoding (cp1252 khong ho tro emoji / tieng Viet)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── Đảm bảo import được auth.py từ thư mục hiện tại ─────────────────
sys.path.insert(0, os.path.dirname(__file__))

# Buộc dùng mock DB
os.environ["USE_MOCK_DB"] = "true"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-12345"

from auth import app, _refresh_blacklist, PERMISSIONS, has_permission


class AuthTestCase(unittest.TestCase):
    """Test suite cho Auth Module."""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        _refresh_blacklist.clear()  # reset blacklist trước mỗi test

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _login(self, username: str, password: str = "123456") -> dict:
        """Đăng nhập và trả về JSON response."""
        res = self.client.post(
            "/auth/login",
            json={"username": username, "password": password},
        )
        return json.loads(res.data), res.status_code

    def _auth_header(self, token: str) -> dict:
        return {"Authorization": f"Bearer {token}"}

    # ==================================================================
    # 1. ĐĂNG NHẬP
    # ==================================================================

    def test_login_success_admin(self):
        """Admin đăng nhập thành công → 200 + tokens."""
        body, code = self._login("admin", "123456")
        self.assertEqual(code, 200)
        self.assertIn("access_token", body)
        self.assertIn("refresh_token", body)
        self.assertEqual(body["user"]["role"], "ADMIN")
        print("✅ [1.1] Đăng nhập ADMIN thành công")

    def test_login_success_lecturer(self):
        """Giảng viên đăng nhập thành công → 200."""
        body, code = self._login("gv001", "123456")
        self.assertEqual(code, 200)
        self.assertEqual(body["user"]["role"], "LECTURER")
        print("✅ [1.2] Đăng nhập LECTURER thành công")

    def test_login_success_student(self):
        """Sinh viên đăng nhập thành công → 200."""
        body, code = self._login("sv20210001", "123456")
        self.assertEqual(code, 200)
        self.assertEqual(body["user"]["role"], "STUDENT")
        print("✅ [1.3] Đăng nhập STUDENT thành công")

    def test_login_wrong_password(self):
        """Sai mật khẩu → 401."""
        body, code = self._login("admin", "wrong_password")
        self.assertEqual(code, 401)
        print("✅ [1.4] Sai mật khẩu → 401")

    def test_login_nonexistent_user(self):
        """User không tồn tại → 401."""
        body, code = self._login("nobody", "123456")
        self.assertEqual(code, 401)
        print("✅ [1.5] User không tồn tại → 401")

    def test_login_locked_account(self):
        """Tài khoản bị khoá → 403."""
        body, code = self._login("locked_user", "123456")
        self.assertEqual(code, 403)
        self.assertIn("khoá", body["message"])
        print("✅ [1.6] Tài khoản bị khoá → 403")

    def test_login_missing_fields(self):
        """Thiếu username / password → 400."""
        res = self.client.post("/auth/login", json={"username": "admin"})
        self.assertEqual(res.status_code, 400)
        print("✅ [1.7] Thiếu trường bắt buộc → 400")

    def test_login_empty_body(self):
        """Body rỗng → 400."""
        res = self.client.post("/auth/login", json={})
        self.assertEqual(res.status_code, 400)
        print("✅ [1.8] Body rỗng → 400")

    # ==================================================================
    # 2. /auth/me – XEM THÔNG TIN BẢN THÂN
    # ==================================================================

    def test_me_with_valid_token(self):
        """/auth/me với access_token hợp lệ → 200."""
        body, _ = self._login("admin")
        res = self.client.get("/auth/me", headers=self._auth_header(body["access_token"]))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["user"]["username"], "admin")
        print("✅ [2.1] /auth/me với token hợp lệ → 200")

    def test_me_without_token(self):
        """/auth/me không có token → 401."""
        res = self.client.get("/auth/me")
        self.assertEqual(res.status_code, 401)
        print("✅ [2.2] /auth/me không có token → 401")

    def test_me_with_invalid_token(self):
        """/auth/me với token giả → 422."""
        res = self.client.get("/auth/me", headers=self._auth_header("totally.fake.token"))
        self.assertIn(res.status_code, [401, 422])
        print("✅ [2.3] /auth/me với token giả → 401/422")

    # ==================================================================
    # 3. REFRESH TOKEN
    # ==================================================================

    def test_refresh_success(self):
        """Đổi refresh_token → access_token mới."""
        body, _ = self._login("admin")
        res = self.client.post(
            "/auth/refresh",
            headers=self._auth_header(body["refresh_token"]),
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("access_token", data)
        print("✅ [3.1] Refresh token thành công → access_token mới")

    def test_refresh_with_access_token_fails(self):
        """Dùng access_token để refresh → 422 (sai loại token)."""
        body, _ = self._login("admin")
        res = self.client.post(
            "/auth/refresh",
            headers=self._auth_header(body["access_token"]),  # sai!
        )
        self.assertIn(res.status_code, [401, 422])
        print("✅ [3.2] Dùng access_token để refresh → lỗi")

    # ==================================================================
    # 4. LOGOUT (BLACKLIST)
    # ==================================================================

    def test_logout_success(self):
        """Logout → refresh_token bị blacklist → không thể refresh nữa."""
        body, _ = self._login("admin")
        refresh_token = body["refresh_token"]

        # Logout
        res_logout = self.client.post(
            "/auth/logout",
            headers=self._auth_header(refresh_token),
        )
        self.assertEqual(res_logout.status_code, 200)

        # Thử refresh sau khi logout → 401
        res_refresh = self.client.post(
            "/auth/refresh",
            headers=self._auth_header(refresh_token),
        )
        self.assertEqual(res_refresh.status_code, 401)
        print("✅ [4.1] Logout → refresh bị thu hồi → 401")

    # ==================================================================
    # 5. PHÂN QUYỀN RBAC – ENDPOINT MẪU
    # ==================================================================

    def test_admin_can_access_admin_endpoint(self):
        """ADMIN truy cập /admin/users → 200."""
        body, _ = self._login("admin")
        res = self.client.get("/admin/users", headers=self._auth_header(body["access_token"]))
        self.assertEqual(res.status_code, 200)
        print("✅ [5.1] ADMIN truy cập /admin/users → 200")

    def test_lecturer_cannot_access_admin_endpoint(self):
        """LECTURER truy cập /admin/users → 403."""
        body, _ = self._login("gv001")
        res = self.client.get("/admin/users", headers=self._auth_header(body["access_token"]))
        self.assertEqual(res.status_code, 403)
        print("✅ [5.2] LECTURER truy cập /admin/users → 403")

    def test_student_cannot_access_admin_endpoint(self):
        """STUDENT truy cập /admin/users → 403."""
        body, _ = self._login("sv20210001")
        res = self.client.get("/admin/users", headers=self._auth_header(body["access_token"]))
        self.assertEqual(res.status_code, 403)
        print("✅ [5.3] STUDENT truy cập /admin/users → 403")

    def test_all_roles_can_read_subjects(self):
        """Cả 3 vai trò đều xem được /subjects → 200."""
        for username, role in [("admin", "ADMIN"), ("gv001", "LECTURER"), ("sv20210001", "STUDENT")]:
            body, _ = self._login(username)
            res = self.client.get("/subjects", headers=self._auth_header(body["access_token"]))
            self.assertEqual(res.status_code, 200, msg=f"{role} phải đọc được /subjects")
        print("✅ [5.4] ADMIN, LECTURER, STUDENT đều đọc được /subjects")

    def test_admin_can_create_subject(self):
        """ADMIN tạo môn học → 201."""
        body, _ = self._login("admin")
        res = self.client.post(
            "/subjects",
            json={"name": "Test Subject", "credits": 3},
            headers=self._auth_header(body["access_token"]),
        )
        self.assertEqual(res.status_code, 201)
        print("✅ [5.5] ADMIN tạo môn học → 201")

    def test_student_cannot_create_subject(self):
        """STUDENT không được tạo môn học → 403."""
        body, _ = self._login("sv20210001")
        res = self.client.post(
            "/subjects",
            json={"name": "Hack Subject"},
            headers=self._auth_header(body["access_token"]),
        )
        self.assertEqual(res.status_code, 403)
        print("✅ [5.6] STUDENT tạo môn học → 403")

    def test_student_can_register_section(self):
        """STUDENT đăng ký học phần → 201."""
        body, _ = self._login("sv20210001")
        res = self.client.post(
            "/registrations",
            json={"section_id": 1},
            headers=self._auth_header(body["access_token"]),
        )
        self.assertEqual(res.status_code, 201)
        print("✅ [5.7] STUDENT đăng ký học phần → 201")

    def test_lecturer_cannot_register_section(self):
        """LECTURER không có quyền đăng ký học phần → 403."""
        body, _ = self._login("gv001")
        res = self.client.post(
            "/registrations",
            json={"section_id": 1},
            headers=self._auth_header(body["access_token"]),
        )
        self.assertEqual(res.status_code, 403)
        print("✅ [5.8] LECTURER đăng ký học phần → 403")

    # ==================================================================
    # 6. KIỂM TRA BẢNG QUYỀN
    # ==================================================================

    def test_permission_matrix(self):
        """Xác minh ma trận quyền RBAC."""
        # ADMIN có tất cả quyền quan trọng
        self.assertTrue(has_permission("ADMIN", "user:delete"))
        self.assertTrue(has_permission("ADMIN", "section:delete"))
        self.assertTrue(has_permission("ADMIN", "report:read"))

        # LECTURER không xoá được user
        self.assertFalse(has_permission("LECTURER", "user:delete"))
        self.assertFalse(has_permission("LECTURER", "registration:create"))

        # STUDENT không xoá user, không tạo môn học
        self.assertFalse(has_permission("STUDENT", "user:delete"))
        self.assertFalse(has_permission("STUDENT", "subject:create"))

        # STUDENT có thể đăng ký học phần
        self.assertTrue(has_permission("STUDENT", "registration:create"))

        print("✅ [6.1] Ma trận quyền RBAC đúng")

    def test_unknown_role_has_no_permissions(self):
        """Vai trò không xác định → không có quyền nào."""
        self.assertFalse(has_permission("HACKER", "user:read"))
        print("✅ [6.2] Vai trò không xác định → không có quyền")

    # ==================================================================
    # 7. /auth/permissions
    # ==================================================================

    def test_permissions_endpoint_admin(self):
        """/auth/permissions trả về đúng danh sách quyền cho ADMIN."""
        body, _ = self._login("admin")
        res = self.client.get(
            "/auth/permissions",
            headers=self._auth_header(body["access_token"]),
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["role"], "ADMIN")
        self.assertIn("user:delete", data["permissions"])
        self.assertIn("report:read", data["permissions"])
        print("✅ [7.1] /auth/permissions trả về đúng quyền ADMIN")

    def test_permissions_endpoint_student(self):
        """/auth/permissions trả về đúng danh sách quyền cho STUDENT."""
        body, _ = self._login("sv20210001")
        res = self.client.get(
            "/auth/permissions",
            headers=self._auth_header(body["access_token"]),
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["role"], "STUDENT")
        self.assertNotIn("user:delete", data["permissions"])
        self.assertIn("registration:create", data["permissions"])
        print("✅ [7.2] /auth/permissions trả về đúng quyền STUDENT")


# =======================================================================
# CHẠY TEST
# =======================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  QLDT Auth Module – Test Suite")
    print("=" * 60)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(AuthTestCase)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    total = result.testsRun
    failed = len(result.failures) + len(result.errors)
    passed = total - failed
    print(f"  Tổng: {total}  |  Passed: {passed}  |  Failed: {failed}")
    print("=" * 60)

    sys.exit(0 if result.wasSuccessful() else 1)
