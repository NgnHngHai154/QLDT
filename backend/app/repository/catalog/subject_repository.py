from sqlalchemy import func, or_, select

from app.entity.catalog.course_section import CourseSection
from app.entity.catalog.subject import Subject
from app.repository.base import BaseRepository


class SubjectRepository(BaseRepository):
    def search(
        self, keyword: str | None, offset: int, limit: int, sort: str | None
    ) -> tuple[list[Subject], int]:
        """Trả (danh sách Subject, tổng số). keyword khớp subjectCode hoặc name."""
        stmt = select(Subject)
        count_stmt = select(func.count(Subject.id))

        if keyword:
            kw = f"%{keyword.strip()}%"
            condition = or_(Subject.subject_code.ilike(kw), Subject.name.ilike(kw))
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)

        total = self.db.scalar(count_stmt) or 0

        # Mặc định sắp theo subject_code tăng dần
        stmt = stmt.order_by(Subject.subject_code.asc()).offset(offset).limit(limit)
        items = list(self.db.scalars(stmt).all())
        return items, total

    def get_by_id(self, subject_id: int) -> Subject | None:
        return self.db.get(Subject, subject_id)

    def exists_by_code(self, subject_code: str) -> bool:
        stmt = select(Subject.id).where(Subject.subject_code == subject_code)
        return self.db.scalars(stmt).first() is not None

    def count_sections(self, subject_id: int) -> int:
        """Số lớp học phần của môn (cho trường sectionCount và chặn xóa)."""
        stmt = select(func.count(CourseSection.id)).where(CourseSection.subject_id == subject_id)
        return self.db.scalar(stmt) or 0

    def add(self, subject: Subject) -> Subject:
        self.db.add(subject)
        self.db.flush()  # lấy id, chưa commit
        return subject

    def delete(self, subject: Subject) -> None:
        self.db.delete(subject)
        self.db.flush()
