from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.timeutil import now_vn_naive
from app.entity.base import Base, BigInt

if TYPE_CHECKING:
    from app.entity.auth.student import Student
    from app.entity.catalog.course_section import CourseSection


class Registration(Base):
    __tablename__ = "REGISTRATIONS"
    __table_args__ = (
        UniqueConstraint("student_id", "section_id", name="uq_registrations_student_section"),
        Index("ix_registrations_section", "section_id"),
        Index("ix_registrations_student", "student_id"),
    )

    id: Mapped[int] = mapped_column("registration_id", BigInt, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(
        BigInt,
        ForeignKey("STUDENTS.student_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    section_id: Mapped[int] = mapped_column(
        BigInt,
        ForeignKey("COURSE_SECTIONS.section_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    registered_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=now_vn_naive,  # lưu giờ VN, xem core/timeutil.py
        server_default=func.current_timestamp(),
    )

    student: Mapped["Student"] = relationship()
    section: Mapped["CourseSection"] = relationship()
