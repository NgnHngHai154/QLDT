import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Alert, Button, Card, Empty, Select, Spin, Table, Tag } from "antd";
import api, { requireItems } from "../../shared/api/client";

interface Semester {
  semesterId: number;
  semesterCode: string;
  name: string;
}

interface Subject {
  subjectId: number;
  subjectCode: string;
  name: string;
  credits: number;
  description: string | null;
}

interface Section {
  sectionId: number;
  sectionCode: string;
  subject: { subjectCode: string; name: string };
  lecturer?: { fullName: string } | null;
  room?: { roomCode: string } | null;
  dayOfWeek: number;
  startPeriod: number;
  endPeriod: number;
  currentEnrollment: number;
  maxCapacity: number;
}

interface ItemsResponse<T> {
  items: T[];
}

export default function AdminCatalogPage({ resource }: { resource: "subjects" | "sections" }) {
  const [page, setPage] = useState(1);
  const [semesterId, setSemesterId] = useState<number>();
  const pageSize = 10;
  const isSubjects = resource === "subjects";

  const semestersQuery = useQuery({
    queryKey: ["semesters"],
    enabled: !isSubjects,
    queryFn: async () => requireItems<Semester>((await api.get<ItemsResponse<Semester>>("/semesters")).data),
  });

  useEffect(() => {
    if (!isSubjects && semesterId === undefined && semestersQuery.data && semestersQuery.data.length > 0) {
      setSemesterId(semestersQuery.data[0].semesterId);
    }
  }, [isSubjects, semestersQuery.data, semesterId]);

  const subjectsQuery = useQuery({
    queryKey: ["subjects", page],
    enabled: isSubjects,
    queryFn: async () => requireItems<Subject>((await api.get<ItemsResponse<Subject>>("/subjects", {
      params: { page, size: pageSize },
    })).data),
  });

  const sectionsQuery = useQuery({
    queryKey: ["sections", "admin", semesterId, page],
    enabled: !isSubjects && semesterId !== undefined,
    queryFn: async () => requireItems<Section>((await api.get<ItemsResponse<Section>>("/sections", {
      params: { semesterId, page, size: pageSize },
    })).data),
  });

  const query = isSubjects ? subjectsQuery : sectionsQuery;
  const rows = query.data ?? [];

  return (
    <>
      {!isSubjects && (
        <div className="feature-toolbar">
          <Select
            aria-label="Học kỳ"
            className="semester-select"
            placeholder="Chọn học kỳ"
            loading={semestersQuery.isLoading}
            value={semesterId}
            options={(semestersQuery.data ?? []).map((semester) => ({ value: semester.semesterId, label: `${semester.semesterCode} · ${semester.name}` }))}
            onChange={(value) => { setSemesterId(value); setPage(1); }}
          />
        </div>
      )}

      <Alert
        className="contract-notice"
        type="info"
        showIcon
        message="Danh sách đang ở chế độ tra cứu"
        description="Schema request/response ghi, validation và mã lỗi CRUD cần đối chiếu contracts/openapi.yaml trước khi bật tạo, sửa hoặc xóa."
      />

      {!isSubjects && semesterId === undefined && <div className="feature-empty"><Empty description="Chọn học kỳ để xem lớp học phần." /></div>}
      {query.isLoading && <div className="feature-loading"><Spin /></div>}
      {query.isError && <Alert type="error" showIcon message="Không tải được danh mục." action={<Button size="small" onClick={() => void query.refetch()}>Thử lại</Button>} />}
      {!query.isLoading && !query.isError && (isSubjects ? rows.length === 0 : semesterId !== undefined && rows.length === 0) && (
        <div className="feature-empty"><Empty description="Chưa có dữ liệu." /></div>
      )}

      {isSubjects && rows.length > 0 && (
        <Table
          rowKey="subjectId"
          dataSource={rows as Subject[]}
          pagination={false}
          scroll={{ x: 680 }}
          columns={[
            { title: "Mã môn", dataIndex: "subjectCode", key: "subjectCode" },
            { title: "Tên môn học", dataIndex: "name", key: "name" },
            { title: "Tín chỉ", dataIndex: "credits", key: "credits", width: 100 },
          ]}
        />
      )}

      {isSubjects && rows.length > 0 && (
        <div className="feature-pagination">
          <Button disabled={page === 1} onClick={() => setPage((value) => value - 1)}>Trước</Button>
          <span>Trang {page}</span>
          <Button disabled={rows.length < pageSize} onClick={() => setPage((value) => value + 1)}>Tiếp</Button>
        </div>
      )}

      {!isSubjects && rows.length > 0 && (
        <div className="section-grid">
          {(rows as Section[]).map((section) => (
            <Card className="section-card" key={section.sectionId}>
              <div className="section-card-top"><span className="section-code">{section.sectionCode}</span><Tag>{section.currentEnrollment}/{section.maxCapacity}</Tag></div>
              <h3>{section.subject.name}</h3>
              <p className="section-subtitle">{section.subject.subjectCode}</p>
              <div className="section-details">
                <span>Thứ {section.dayOfWeek} · Tiết {section.startPeriod}-{section.endPeriod}</span>
                {section.lecturer?.fullName && <span>{section.lecturer.fullName}</span>}
                {section.room?.roomCode && <span>Phòng {section.room.roomCode}</span>}
              </div>
            </Card>
          ))}
        </div>
      )}
    </>
  );
}