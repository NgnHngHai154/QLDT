from datetime import timedelta

from sqlalchemy.orm import Session

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppError, field_error
from app.core.timeutil import today_vn
from app.dto.catalog.catalog import Section
from app.dto.common import ItemList
from app.dto.timetable.timetable import Timetable, TimetableItem
from app.entity.auth.user import User
from app.repository.auth.user_repository import LecturerRepository, StudentRepository
from app.repository.catalog.section_repository import SectionRepository
from app.repository.catalog.semester_repository import SemesterRepository
from app.repository.registration.registration_repository import RegistrationRepository
from app.service.catalog.semester_service import week_of


class TimetableService:
    """UC007 (thời khóa biểu sinh viên), UC008 (lịch dạy giảng viên)."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.semesters = SemesterRepository(db)
        self.sections = SectionRepository(db)
        self.registrations = RegistrationRepository(db)
        self.students = StudentRepository(db)
        self.lecturers = LecturerRepository(db)

    def _resolve_week_and_dates(self, semester_id: int, week: int | None):
        semester = self.semesters.get_by_id(semester_id)
        if semester is None:
            raise AppError(
                ErrorCode.NOT_FOUND, details=[field_error("semesterId", "Học kỳ không tồn tại")]
            )

        if week is None:
            current = week_of(semester, today_vn())
            target_week = current if current is not None else 1
        else:
            target_week = week

        if target_week < 1 or target_week > semester.num_weeks:
            raise AppError(
                ErrorCode.INVALID_WEEK,
                details=[
                    field_error("week", f"Tuần phải nằm trong khoảng từ 1 đến {semester.num_weeks}")
                ],
            )

        week_start_date = semester.start_date + timedelta(days=(target_week - 1) * 7)
        week_end_date = week_start_date + timedelta(days=6)
        return semester, target_week, week_start_date, week_end_date

    def student_timetable(self, user: User, semester_id: int, week: int | None) -> Timetable:
        student = self.students.get_by_user_id(user.id)
        if student is None:
            raise AppError(ErrorCode.FORBIDDEN)

        semester, target_week, week_start_date, week_end_date = self._resolve_week_and_dates(
            semester_id, week
        )

        regs = self.registrations.list_by_student(student.id, semester.id)
        items: list[TimetableItem] = []
        for r in regs:
            s = r.section
            if s.start_week <= target_week <= s.end_week:
                class_date = week_start_date + timedelta(days=s.day_of_week - 2)
                items.append(
                    TimetableItem(
                        section_id=s.id,
                        section_code=s.section_code,
                        subject_code=s.subject.subject_code,
                        subject_name=s.subject.name,
                        day_of_week=s.day_of_week,
                        date=class_date,
                        start_period=s.start_period,
                        end_period=s.end_period,
                        room_code=s.room.room_code,
                        lecturer_name=s.lecturer.full_name,
                        start_week=s.start_week,
                        end_week=s.end_week,
                    )
                )

        items.sort(key=lambda x: (x.day_of_week, x.start_period))
        return Timetable(
            semester_id=semester.id,
            week=target_week,
            week_start_date=week_start_date,
            week_end_date=week_end_date,
            items=items,
        )

    def lecturer_timetable(self, user: User, semester_id: int, week: int | None) -> Timetable:
        lecturer = self.lecturers.get_by_user_id(user.id)
        if lecturer is None:
            raise AppError(ErrorCode.FORBIDDEN)

        semester, target_week, week_start_date, week_end_date = self._resolve_week_and_dates(
            semester_id, week
        )

        sections = self.sections.list_by_lecturer(lecturer.id, semester.id)
        items: list[TimetableItem] = []
        for s in sections:
            if s.start_week <= target_week <= s.end_week:
                class_date = week_start_date + timedelta(days=s.day_of_week - 2)
                items.append(
                    TimetableItem(
                        section_id=s.id,
                        section_code=s.section_code,
                        subject_code=s.subject.subject_code,
                        subject_name=s.subject.name,
                        day_of_week=s.day_of_week,
                        date=class_date,
                        start_period=s.start_period,
                        end_period=s.end_period,
                        room_code=s.room.room_code,
                        lecturer_name=s.lecturer.full_name,
                        start_week=s.start_week,
                        end_week=s.end_week,
                    )
                )

        items.sort(key=lambda x: (x.day_of_week, x.start_period))
        return Timetable(
            semester_id=semester.id,
            week=target_week,
            week_start_date=week_start_date,
            week_end_date=week_end_date,
            items=items,
        )

    def lecturer_sections(self, user: User, semester_id: int) -> ItemList[Section]:
        lecturer = self.lecturers.get_by_user_id(user.id)
        if lecturer is None:
            raise AppError(ErrorCode.FORBIDDEN)

        sections = self.sections.list_by_lecturer(lecturer.id, semester_id)
        items = [Section.model_validate(s) for s in sections]
        return ItemList[Section](items=items)
