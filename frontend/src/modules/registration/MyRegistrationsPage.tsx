import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { App, Alert, Button, Card, Empty, Select, Spin, Tag, message } from "antd";
import api, { readApiError, requireItems } from "../../shared/api/client";

interface Semester {
  semesterId: number;
  semesterCode: string;
  name: string;
}

interface RegisteredSection {
  sectionId: number;
  sectionCode: string;
  subject: { subjectCode: string; name: string; credits: number };
  dayOfWeek: number;
  startPeriod: number;
  endPeriod: number;
  startWeek: number;
  endWeek: number;
}

interface Registration {
  registrationId: number;
  section: RegisteredSection;
}

interface ItemsResponse<T> {
  items: T[];
}

const days: Record<number, string> = {
  2: "Thứ hai", 3: "Thứ ba", 4: "Thứ tư", 5: "Thứ năm",
  6: "Thứ sáu", 7: "Thứ bảy", 8: "Chủ nhật",
};

export default function MyRegistrationsPage() {
  const { modal } = App.useApp();
  const queryClient = useQueryClient();
  const [semesterId, setSemesterId] = useState<number>();
  const [messageApi, contextHolder] = message.useMessage();

  const semestersQuery = useQuery({
    queryKey: ["semesters"],
    queryFn: async () => requireItems<Semester>((await api.get<ItemsResponse<Semester>>("/semesters")).data),
  });

  const registrationsQuery = useQuery({
    queryKey: ["registrations", semesterId],
    enabled: semesterId !== undefined,
    queryFn: async () => requireItems<Registration>((await api.get<ItemsResponse<Registration>>("/registrations/me", {
      params: { semesterId },
    })).data),
  });

  const cancelMutation = useMutation({
    mutationFn: (registrationId: number) => api.delete(`/registrations/${registrationId}`),
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["registrations", semesterId] }),
        queryClient.invalidateQueries({ queryKey: ["sections", semesterId] }),
        queryClient.invalidateQueries({ queryKey: ["timetable"] }),
      ]);
      messageApi.success("Đã hủy đăng ký.");
    },
    onError: (error: unknown) => {
      const body = readApiError(error);
      if (body?.error === "FORBIDDEN") messageApi.error("Bạn không có quyền hủy đăng ký này.");
      else if (body?.error === "CREDIT_LIMIT_BELOW_MIN") {
        const details = body.details.map((detail) => detail.message).filter(Boolean);
        messageApi.error(
          details.length
            ? `Không thể hủy. ${details.join("; ")}`
            : "Không thể hủy vì số tín chỉ sẽ thấp hơn mức tối thiểu của học kỳ.",
        );
      } else messageApi.error("Không thể hủy đăng ký lúc này. Vui lòng tải lại danh sách.");
    },
  });

  function confirmCancellation(registration: Registration) {
    modal.confirm({
      title: "Hủy đăng ký học phần?",
      content: `${registration.section.subject.name} · ${registration.section.sectionCode}`,
      okText: "Hủy đăng ký",
      okButtonProps: { danger: true },
      cancelText: "Giữ đăng ký",
      onOk: () => cancelMutation.mutateAsync(registration.registrationId),
    });
  }

  return (
    <>
      {contextHolder}
      <div className="feature-toolbar">
        <Select
          aria-label="Học kỳ"
          className="semester-select"
          placeholder="Chọn học kỳ"
          loading={semestersQuery.isLoading}
          value={semesterId}
          options={(semestersQuery.data ?? []).map((semester) => ({ value: semester.semesterId, label: `${semester.semesterCode} · ${semester.name}` }))}
          onChange={setSemesterId}
        />
      </div>
      {semestersQuery.isError && <Alert type="error" showIcon message="Không tải được danh sách học kỳ." action={<Button size="small" onClick={() => void semestersQuery.refetch()}>Thử lại</Button>} />}
      {semesterId === undefined && !semestersQuery.isError && <div className="feature-empty"><Empty description="Chọn học kỳ để xem các lớp đã đăng ký." /></div>}
      {registrationsQuery.isLoading && <div className="feature-loading"><Spin /></div>}
      {registrationsQuery.isError && <Alert type="error" showIcon message="Không tải được đăng ký học phần." action={<Button size="small" onClick={() => void registrationsQuery.refetch()}>Thử lại</Button>} />}
      {registrationsQuery.data?.length === 0 && <div className="feature-empty"><Empty description="Chưa có lớp học phần trong học kỳ này." /></div>}
      <div className="registration-list">
        {(registrationsQuery.data ?? []).map((registration) => {
          const section = registration.section;
          return (
            <Card key={registration.registrationId} className="registration-card">
              <div className="registration-card-main">
                <div>
                  <div className="section-card-top"><span className="section-code">{section.sectionCode}</span><Tag color="blue">{section.subject.credits} tín chỉ</Tag></div>
                  <h3>{section.subject.name}</h3>
                  <p className="section-subtitle">{section.subject.subjectCode}</p>
                  <div className="section-details">
                    <span>{days[section.dayOfWeek] ?? `Thứ ${section.dayOfWeek}`} · Tiết {section.startPeriod}-{section.endPeriod}</span>
                    <span>Tuần {section.startWeek}-{section.endWeek}</span>
                  </div>
                </div>
                <Button danger loading={cancelMutation.isPending && cancelMutation.variables === registration.registrationId} onClick={() => confirmCancellation(registration)}>
                  Hủy đăng ký
                </Button>
              </div>
            </Card>
          );
        })}
      </div>
    </>
  );
}