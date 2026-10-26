from sqlalchemy.orm import Session

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppError, field_error
from app.dto.common import ItemList
from app.dto.registration.registration import RegisterRequest
from app.dto.registration.registration import Registration as RegistrationDto
from app.entity.auth.user import User
from app.entity.registration.registration import Registration as RegistrationEntity
from app.repository.auth.user_repository import StudentRepository
from app.repository.catalog.section_repository import SectionRepository
from app.repository.registration.registration_repository import RegistrationRepository


class RegistrationService:
    """UC005 (đăng ký) và UC006 (hủy). Mỗi thao tác ghi là MỘT giao dịch: db.commit() ở cuối,
    lỗi nghiệp vụ -> ném AppError (get_db sẽ rollback)."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.students = StudentRepository(db)
        self.sections = SectionRepository(db)
        self.registrations = RegistrationRepository(db)

    def register(self, user: User, request: RegisterRequest) -> RegistrationDto:
        student = self.students.get_by_user_id(user.id)
        if student is None:
            raise AppError(ErrorCode.FORBIDDEN)

        section = self.sections.get_by_id(request.section_id)
        if section is None:
            raise AppError(
                ErrorCode.NOT_FOUND,
                details=[field_error("sectionId", "Lớp học phần không tồn tại")],
            )

        if self.registrations.exists(student.id, section.id):
            raise AppError(ErrorCode.ALREADY_REGISTERED)

        same_subject = self.registrations.find_same_subject(
            student.id, section.subject_id, section.semester_id
        )
        if same_subject is not None:
            raise AppError(
                ErrorCode.SAME_SUBJECT_REGISTERED,
                details=[
                    field_error(
                        "sectionId",
                        f"Bạn đã đăng ký lớp {same_subject.section.section_code} của môn học này",
                    )
                ],
            )

        conflicts = self.registrations.find_schedule_conflicts(student.id, section)
        if conflicts:
            conflict_details = [
                field_error(
                    "sectionId",
                    f"Trùng lịch với lớp {c.section_code} ({c.subject.name})",
                )
                for c in conflicts
            ]
            raise AppError(ErrorCode.STUDENT_SCHEDULE_CONFLICT, details=conflict_details)

        # Cập nhật sĩ số có điều kiện (atomic)
        available = self.sections.increment_enrollment_if_available(section.id)
        if not available:
            raise AppError(ErrorCode.CLASS_FULL)

        reg = RegistrationEntity(student_id=student.id, section_id=section.id)
        self.registrations.add(reg)
        self.db.commit()

        # Nạp lại dữ liệu sau khi commit
        loaded_reg = self.registrations.get_by_id(reg.id)
        dto = RegistrationDto.model_validate(loaded_reg)
        dto.section.registered_by_me = True
        return dto

    def cancel(self, user: User, registration_id: int) -> None:
        student = self.students.get_by_user_id(user.id)
        if student is None:
            raise AppError(ErrorCode.FORBIDDEN)

        reg = self.registrations.get_by_id(registration_id)
        if reg is None:
            raise AppError(ErrorCode.NOT_FOUND)

        if reg.student_id != student.id:
            raise AppError(ErrorCode.FORBIDDEN)

        self.sections.decrement_enrollment(reg.section_id)
        self.registrations.delete(reg)
        self.db.commit()

    def list_mine(self, user: User, semester_id: int) -> ItemList[RegistrationDto]:
        student = self.students.get_by_user_id(user.id)
        if student is None:
            return ItemList[RegistrationDto](items=[])

        regs = self.registrations.list_by_student(student.id, semester_id)
        items: list[RegistrationDto] = []
        for r in regs:
            dto = RegistrationDto.model_validate(r)
            dto.section.registered_by_me = True
            items.append(dto)

        return ItemList[RegistrationDto](items=items)
