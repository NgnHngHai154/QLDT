import { useQuery } from "@tanstack/react-query";
import { Alert, Button, Card, Empty, Spin, Table, Tag } from "antd";
import type { ColumnsType } from "antd/es/table";
import { useNavigate } from "react-router-dom";
import api, { requireItems } from "../../shared/api/client";

interface CourseSection {
  sectionId: number;
  sectionCode: string;
  subject: { subjectCode: string; name: string };
  semester?: { semesterCode: string } | null;
}

interface SectionStudent {
  id: number;
  studentCode: string;
  fullName: string;
  email: string | null;
  cohort: string | null;
  major: string | null;
  registeredAt: string;
}

interface SectionStudentList {
  sectionId: number;
  sectionCode: string;
  currentEnrollment: number;
  maxCapacity: number;
  items: SectionStudent[];
}

interface ItemsResponse<T> {
  items: T[];
}

export function LecturerSectionsPage() {
  const navigate = useNavigate();
  const sectionsQuery = useQuery({
    queryKey: ["lecturer-sections"],
    queryFn: async () => requireItems<CourseSection>((await api.get<ItemsResponse<CourseSection>>("/lecturers/me/sections")).data),
  });

  if (sectionsQuery.isLoading) return <div className="feature-loading"><Spin /></div>;
  if (sectionsQuery.isError) return <Alert type="error" showIcon message="Không tải được lớp phụ trách." action={<Button size="small" onClick={() => void sectionsQuery.refetch()}>Thử lại</Button>} />;
  if (!sectionsQuery.data?.length) return <div className="feature-empty"><Empty description="Bạn chưa có lớp phụ trách." /></div>;

  return (
    <div className="section-grid">
      {sectionsQuery.data.map((section) => (
        <Card className="section-card" key={section.sectionId}>
          <div className="section-card-top"><span className="section-code">{section.sectionCode}</span><Tag color="blue">{section.semester?.semesterCode ?? "2026.1"}</Tag></div>
          <h3>{section.subject.name}</h3>
          <p className="section-subtitle">{section.subject.subjectCode}</p>
          <Button type="primary" onClick={() => navigate(`/app/sections/${section.sectionId}/students`)}>Danh sách sinh viên</Button>
        </Card>
      ))}
    </div>
  );
}

export function SectionRosterPage({ sectionId }: { sectionId: number }) {
  const navigate = useNavigate();
  const rosterQuery = useQuery({
    queryKey: ["section-roster", sectionId],
    queryFn: async () => (await api.get<SectionStudentList>(`/sections/${sectionId}/students`)).data,
  });

  if (rosterQuery.isLoading) return <div className="feature-loading"><Spin /></div>;
  if (rosterQuery.isError) return <Alert type="error" showIcon message="Không tải được danh sách sinh viên của lớp." action={<Button size="small" onClick={() => void rosterQuery.refetch()}>Thử lại</Button>} />;

  const roster = rosterQuery.data;
  const students = roster?.items ?? [];

  const columns: ColumnsType<SectionStudent> = [
    { title: "STT", key: "index", width: 60, align: "center", render: (_, __, i) => i + 1 },
    { title: "MSSV", dataIndex: "studentCode", key: "studentCode", width: 120 },
    { title: "Họ và tên", dataIndex: "fullName", key: "fullName", render: (name: string) => <strong>{name}</strong> },
    { title: "Email", dataIndex: "email", key: "email", render: (val: string | null) => val || "—" },
    { title: "Khóa", dataIndex: "cohort", key: "cohort", width: 90, render: (val: string | null) => val || "—" },
    { title: "Ngành", dataIndex: "major", key: "major", render: (val: string | null) => val || "—" },
    { title: "Thời điểm đăng ký", dataIndex: "registeredAt", key: "registeredAt", width: 180 },
  ];

  return (
    <div className="roster-page">
      <div style={{ marginBottom: 16, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h3 style={{ margin: 0 }}>Lớp học phần: {roster?.sectionCode}</h3>
          <span style={{ color: "#6c757d" }}>Sĩ số hiện tại: <strong>{roster?.currentEnrollment}</strong> / {roster?.maxCapacity} sinh viên</span>
        </div>
        <Button onClick={() => navigate(-1)}>Quay lại</Button>
      </div>
      <Table<SectionStudent>
        rowKey="id"
        size="small"
        dataSource={students}
        columns={columns}
        pagination={{ pageSize: 15, showTotal: (t) => `Tổng ${t} sinh viên` }}
        locale={{ emptyText: <Empty description="Lớp chưa có sinh viên đăng ký." /> }}
      />
    </div>
  );
}
