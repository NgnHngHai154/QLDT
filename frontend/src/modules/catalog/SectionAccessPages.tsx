import { useQuery } from "@tanstack/react-query";
import { Alert, Button, Card, Empty, Spin, Statistic, Tag } from "antd";
import { useNavigate } from "react-router-dom";
import api, { requireItems } from "../../shared/api/client";

interface CourseSection {
  sectionId: number;
  sectionCode: string;
  subject: { subjectCode: string; name: string };
  semester?: { semesterCode: string } | null;
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
          <div className="section-card-top"><span className="section-code">{section.sectionCode}</span><Tag color="blue">{section.semester?.semesterCode ?? "Lớp phụ trách"}</Tag></div>
          <h3>{section.subject.name}</h3>
          <p className="section-subtitle">{section.subject.subjectCode}</p>
          <Button onClick={() => navigate(`/app/sections/${section.sectionId}/students`)}>Danh sách sinh viên</Button>
        </Card>
      ))}
    </div>
  );
}

export function SectionRosterPage({ sectionId }: { sectionId: number }) {
  const rosterQuery = useQuery({
    queryKey: ["section-roster", sectionId],
    queryFn: async () => requireItems<unknown>((await api.get<ItemsResponse<unknown>>(`/sections/${sectionId}/students`)).data),
  });

  if (rosterQuery.isLoading) return <div className="feature-loading"><Spin /></div>;
  if (rosterQuery.isError) return <Alert type="error" showIcon message="Không tải được danh sách sinh viên của lớp." action={<Button size="small" onClick={() => void rosterQuery.refetch()}>Thử lại</Button>} />;
  if (!rosterQuery.data?.length) return <div className="feature-empty"><Empty description="Lớp chưa có sinh viên đăng ký." /></div>;

  return (
    <Card className="roster-summary">
      <Statistic title="Sinh viên trong lớp" value={rosterQuery.data.length} />
      <p>Chi tiết cột thông tin sẽ được hiển thị sau khi đối chiếu schema roster trong OpenAPI.</p>
    </Card>
  );
}