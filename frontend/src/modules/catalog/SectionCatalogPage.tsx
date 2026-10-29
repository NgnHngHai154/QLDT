import { useEffect, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { App, Alert, Button, Card, Empty, Input, Select, Spin, Tag, message } from "antd";
import { SearchOutlined } from "@ant-design/icons";
import api, { readApiError, requireItems } from "../../shared/api/client";
import type { Section, Semester } from "../../shared/api/api-types";
import { fetchSections } from "./catalogApi";

interface ItemsResponse<T> {
  items: T[];
}

const pageSize = 10;

const days: Record<number, string> = {
  2: "Thứ hai",
  3: "Thứ ba",
  4: "Thứ tư",
  5: "Thứ năm",
  6: "Thứ sáu",
  7: "Thứ bảy",
  8: "Chủ nhật",
};

function scheduleLabel(section: Section) {
  return `${days[section.dayOfWeek] ?? `Thứ ${section.dayOfWeek}`} · Tiết ${section.startPeriod}-${section.endPeriod} · Tuần ${section.startWeek}-${section.endWeek}`;
}

export default function SectionCatalogPage() {
  const { modal } = App.useApp();
  const queryClient = useQueryClient();
  const [semesterId, setSemesterId] = useState<number>();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [messageApi, contextHolder] = message.useMessage();

  const semestersQuery = useQuery({
    queryKey: ["semesters"],
    queryFn: async () => requireItems<Semester>((await api.get<ItemsResponse<Semester>>("/semesters")).data),
  });

  useEffect(() => {
    if (semesterId === undefined && semestersQuery.data && semestersQuery.data.length > 0) {
      setSemesterId(semestersQuery.data[0].id);
    }
  }, [semestersQuery.data, semesterId]);

  const sectionsQuery = useQuery({
    queryKey: ["sections", semesterId, page, search],
    enabled: semesterId !== undefined,
    queryFn: () =>
      fetchSections({
        semesterId: semesterId!,
        page,
        size: pageSize,
        keyword: search.trim() || undefined,
      }),
  });
  const sections = sectionsQuery.data?.items ?? [];

  const registrationMutation = useMutation({
    mutationFn: (sectionId: number) => api.post("/registrations", { sectionId }),
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["sections", semesterId] }),
        queryClient.invalidateQueries({ queryKey: ["registrations", semesterId] }),
      ]);
      messageApi.success("Đăng ký thành công.");
    },
    onError: (error: unknown) => {
      const body = readApiError(error);
      if (body?.error === "CREDIT_LIMIT_EXCEEDED") {
        const details = body.details.map((detail) => detail.message).filter(Boolean);
        messageApi.error(
          details.length
            ? `Không thể đăng ký. ${details.join("; ")}`
            : "Đăng ký vượt quá số tín chỉ tối đa trong học kỳ.",
        );
        void queryClient.invalidateQueries({ queryKey: ["sections", semesterId] });
        return;
      }
      const errors: Record<string, string> = {
        CLASS_FULL: "Lớp học phần đã đủ sĩ số.",
        ALREADY_REGISTERED: "Bạn đã đăng ký lớp học phần này.",
        SAME_SUBJECT_REGISTERED: "Bạn đã đăng ký một lớp khác của môn học này.",
        STUDENT_SCHEDULE_CONFLICT: "Lịch học bị trùng với lớp đã đăng ký.",
      };
      messageApi.error(errors[body?.error ?? ""] ?? "Không thể đăng ký lúc này. Vui lòng thử lại.");
      void queryClient.invalidateQueries({ queryKey: ["sections", semesterId] });
    },
  });

  function confirmRegistration(section: Section) {
    modal.confirm({
      title: "Xác nhận đăng ký",
      content: `${section.subject.name} · ${section.sectionCode}`,
      okText: "Đăng ký",
      cancelText: "Để sau",
      onOk: () => registrationMutation.mutateAsync(section.id),
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
          options={(semestersQuery.data ?? []).map((semester) => ({
            value: semester.id,
            label: `${semester.semesterCode} · ${semester.name}`,
          }))}
          onChange={(value: number) => {
            setSemesterId(value);
            setPage(1);
          }}
        />
        <Input
          allowClear
          aria-label="Tìm lớp học phần"
          className="section-search"
          placeholder="Tìm theo mã lớp hoặc môn học"
          prefix={<SearchOutlined />}
          value={search}
          onChange={(event) => {
            setSearch(event.target.value);
            setPage(1);
          }}
        />
      </div>

      {semestersQuery.isError && (
        <Alert type="error" showIcon message="Không tải được danh sách học kỳ." action={<Button size="small" onClick={() => void semestersQuery.refetch()}>Thử lại</Button>} />
      )}
      {!semestersQuery.isError && semesterId === undefined && (
        <div className="feature-empty"><Empty description="Chọn học kỳ để xem lớp học phần." /></div>
      )}
      {sectionsQuery.isLoading && <div className="feature-loading"><Spin /></div>}
      {sectionsQuery.isError && (
        <Alert type="error" showIcon message="Không tải được lớp học phần." action={<Button size="small" onClick={() => void sectionsQuery.refetch()}>Thử lại</Button>} />
      )}
      {semesterId !== undefined && !sectionsQuery.isLoading && !sectionsQuery.isError && sections.length === 0 && (
        <div className="feature-empty"><Empty description={search.trim() ? "Không tìm thấy lớp phù hợp." : "Học kỳ này chưa có lớp học phần."} /></div>
      )}

      <div className="section-grid">
        {sections.map((section) => (
          <Card key={section.id} className="section-card">
            <div className="section-card-top">
              <span className="section-code">{section.sectionCode}</span>
              <Tag color={section.full ? "error" : "success"}>{section.full ? "Đã đầy" : `Còn ${section.remainingSeats} chỗ`}</Tag>
            </div>
            <h3>{section.subject.name}</h3>
            <p className="section-subtitle">{section.subject.subjectCode} · {section.subject.credits} tín chỉ</p>
            <div className="section-details">
              <span>{scheduleLabel(section)}</span>
              {section.lecturer?.fullName && <span>{section.lecturer.fullName}</span>}
              {section.room?.roomCode && <span>Phòng {section.room.roomCode}</span>}
              <span>Sĩ số {section.currentEnrollment}/{section.maxCapacity}</span>
            </div>
            <div className="section-card-action">
              {section.registeredByMe ? (
                <Tag color="blue">Đã đăng ký</Tag>
              ) : (
                <Button
                  type="primary"
                  disabled={section.full}
                  loading={registrationMutation.isPending && registrationMutation.variables === section.id}
                  onClick={() => confirmRegistration(section)}
                >
                  Đăng ký
                </Button>
              )}
            </div>
          </Card>
        ))}
      </div>

      {semesterId !== undefined && (sectionsQuery.data?.totalItems ?? 0) > 0 && (
        <div className="feature-pagination">
          <Button disabled={page <= 1} onClick={() => setPage((value) => value - 1)}>Trước</Button>
          <span>Trang {page}/{sectionsQuery.data?.totalPages ?? 1} · Tổng {sectionsQuery.data?.totalItems ?? 0} lớp</span>
          <Button disabled={page >= (sectionsQuery.data?.totalPages ?? 1)} onClick={() => setPage((value) => value + 1)}>Tiếp</Button>
        </div>
      )}
    </>
  );
}
