from sqlalchemy.orm import Session

from app.core.error_codes import ErrorCode
from app.core.exceptions import AppError, field_error
from app.dto.catalog.catalog import Subject, SubjectCreateRequest, SubjectUpdateRequest
from app.dto.common import Page, PageParams
from app.entity.catalog.subject import Subject as SubjectEntity
from app.repository.catalog.subject_repository import SubjectRepository


class SubjectService:
    """UC002 – quản lý môn học (chỉ ADMIN)."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.subjects = SubjectRepository(db)

    def list(self, keyword: str | None, paging: PageParams) -> Page[Subject]:
        items, total = self.subjects.search(keyword, paging.offset, paging.size, paging.sort)
        dtos: list[Subject] = []
        for s in items:
            dto = Subject.model_validate(s)
            dto.section_count = self.subjects.count_sections(s.id)
            dtos.append(dto)
        return Page.of(dtos, paging, total)

    def get(self, subject_id: int) -> Subject:
        entity = self.subjects.get_by_id(subject_id)
        if entity is None:
            raise AppError(ErrorCode.NOT_FOUND)
        dto = Subject.model_validate(entity)
        dto.section_count = self.subjects.count_sections(entity.id)
        return dto

    def create(self, request: SubjectCreateRequest) -> Subject:
        if self.subjects.exists_by_code(request.subject_code):
            raise AppError(
                ErrorCode.DUPLICATE_CODE,
                details=[field_error("subjectCode", "Mã môn học đã tồn tại")],
            )
        entity = SubjectEntity(
            subject_code=request.subject_code,
            name=request.name,
            credits=request.credits,
            description=request.description,
        )
        self.subjects.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        dto = Subject.model_validate(entity)
        dto.section_count = 0
        return dto

    def update(self, subject_id: int, request: SubjectUpdateRequest) -> Subject:
        entity = self.subjects.get_by_id(subject_id)
        if entity is None:
            raise AppError(ErrorCode.NOT_FOUND)

        entity.name = request.name
        entity.credits = request.credits
        entity.description = request.description

        self.db.commit()
        self.db.refresh(entity)
        dto = Subject.model_validate(entity)
        dto.section_count = self.subjects.count_sections(entity.id)
        return dto

    def delete(self, subject_id: int) -> None:
        entity = self.subjects.get_by_id(subject_id)
        if entity is None:
            raise AppError(ErrorCode.NOT_FOUND)

        if self.subjects.count_sections(subject_id) > 0:
            raise AppError(ErrorCode.SUBJECT_HAS_SECTIONS)

        self.subjects.delete(entity)
        self.db.commit()
