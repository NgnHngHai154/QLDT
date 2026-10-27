import { useMemo, useState } from "react";
import {
  Alert,
  Button,
  Card,
  Form,
  InputNumber,
  Select,
  Space,
  Table,
  Tag,
  Typography,
} from "antd";
import type { ColumnsType } from "antd/es/table";

type Assignment = {
  id: number;
  sectionCode: string;
  subjectName: string;
  lecturer: string;
  room: string;
  dayOfWeek: number;
  startPeriod: number;
  endPeriod: number;
  weeks: string;
};

const lecturerOptions = ["Nguyễn Văn An", "Trần Thị Bình", "Lê Minh Châu"];
const roomOptions = ["B1-101", "B1-202", "C2-301", "Lab-AI-01"];
const dayOptions = [2, 3, 4, 5, 6, 7, 8].map((day) => ({
  value: day,
  label: "Thứ " + day,
}));

const initialAssignments: Assignment[] = [
  {
    id: 1,
    sectionCode: "IT3011-01",
    subjectName: "Cấu trúc dữ liệu và giải thuật",
    lecturer: "Nguyễn Văn An",
    room: "B1-101",
    dayOfWeek: 2,
    startPeriod: 1,
    endPeriod: 3,
    weeks: "1-15",
  },
  {
    id: 2,
    sectionCode: "IT3030-02",
    subjectName: "Kiến trúc máy tính",
    lecturer: "Trần Thị Bình",
    room: "Lab-AI-01",
    dayOfWeek: 2,
    startPeriod: 1,
    endPeriod: 3,
    weeks: "1-15",
  },
  {
    id: 3,
    sectionCode: "IT3100-01",
    subjectName: "Lập trình hướng đối tượng",
    lecturer: "Lê Minh Châu",
    room: "B1-202",
    dayOfWeek: 4,
    startPeriod: 4,
    endPeriod: 6,
    weeks: "1-15",
  },
];

function overlaps(left: Assignment, right: Assignment) {
  return (
    left.dayOfWeek === right.dayOfWeek &&
    left.weeks === right.weeks &&
    left.startPeriod <= right.endPeriod &&
    right.startPeriod <= left.endPeriod
  );
}

export default function AdminTimetablePage() {
  const [assignments, setAssignments] = useState(initialAssignments);
  const [selectedId, setSelectedId] = useState(initialAssignments[0].id);
  const [error, setError] = useState("");
  const selected = assignments.find((item) => item.id === selectedId) ?? assignments[0];

  const lecturerConflicts = useMemo(
    () =>
      assignments.filter(
        (item) =>
          item.id !== selected.id &&
          item.lecturer === selected.lecturer &&
          overlaps(item, selected),
      ),
    [assignments, selected],
  );
  const roomConflicts = useMemo(
    () =>
      assignments.filter(
        (item) => item.id !== selected.id && item.room === selected.room && overlaps(item, selected),
      ),
    [assignments, selected],
  );

  const saveAssignment = (values: Partial<Assignment>) => {
    const next: Assignment = {
      ...selected,
      ...values,
      dayOfWeek: Number(values.dayOfWeek ?? selected.dayOfWeek),
      startPeriod: Number(values.startPeriod ?? selected.startPeriod),
      endPeriod: Number(values.endPeriod ?? selected.endPeriod),
    };

    if (next.startPeriod > next.endPeriod || next.startPeriod < 1 || next.endPeriod > 12) {
      setError("Tiết bắt đầu phải nhỏ hơn hoặc bằng tiết kết thúc và nằm trong khoảng 1-12.");
      return;
    }

    const conflict = assignments.find(
      (item) =>
        item.id !== next.id &&
        overlaps(item, next) &&
        (item.room === next.room || item.lecturer === next.lecturer),
    );
    if (conflict) {
      const conflictType =
        conflict.room === next.room && conflict.lecturer === next.lecturer
          ? "phòng học và giảng viên"
          : conflict.room === next.room
            ? "phòng học"
            : "giảng viên";
      setError(
        "Không thể lưu: " +
          conflictType +
          " đang bị trùng với lớp " +
          conflict.sectionCode +
          " trong cùng ngày, tiết và tuần học.",
      );
      return;
    }

    setAssignments((current) => current.map((item) => (item.id === next.id ? next : item)));
    setError("");
  };

  const columns: ColumnsType<Assignment> = [
    {
      title: "Lớp HP",
      dataIndex: "sectionCode",
      width: 120,
      render: (value: string, record) => (
        <Button type="link" onClick={() => setSelectedId(record.id)} style={{ padding: 0 }}>
          {value}
        </Button>
      ),
    },
    {
      title: "Tên học phần",
      dataIndex: "subjectName",
      render: (value: string) => <Typography.Text strong>{value}</Typography.Text>,
    },
    { title: "Giảng viên", dataIndex: "lecturer", width: 170 },
    {
      title: "Phòng",
      dataIndex: "room",
      width: 120,
      render: (value: string) => <Tag color="blue">{value}</Tag>,
    },
    {
      title: "Lịch học",
      width: 150,
      render: (_, record) =>
        "Thứ " +
        record.dayOfWeek +
        ", tiết " +
        record.startPeriod +
        "-" +
        record.endPeriod,
    },
    { title: "Tuần", dataIndex: "weeks", width: 80 },
    {
      title: "Thao tác",
      width: 100,
      render: (_, record) => (
        <Button size="small" onClick={() => setSelectedId(record.id)}>
          Chỉnh sửa
        </Button>
      ),
    },
  ];

  return (
    <div className="admin-timetable-page">
      <style>{`
        .admin-timetable-page { padding: 24px; background: #f5f7fb; min-height: calc(100vh - 64px); }
        .admin-timetable-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; margin-bottom: 18px; }
        .admin-timetable-header h2 { margin: 0 0 4px; }
        .admin-timetable-grid { display: grid; grid-template-columns: minmax(0, 1fr) 330px; gap: 18px; align-items: start; }
        .admin-timetable-form .ant-form-item { margin-bottom: 14px; }
        @media (max-width: 1100px) { .admin-timetable-grid { grid-template-columns: 1fr; } }
      `}</style>
      <div className="admin-timetable-header">
        <div>
          <Typography.Title level={2}>Xếp lịch &amp; phân công</Typography.Title>
          <Typography.Text type="secondary">
            Quản lý lịch học, phòng máy/giảng đường và giảng viên theo từng lớp học phần.
          </Typography.Text>
        </div>
        <Tag color="geekblue">QUẢN TRỊ / PHÒNG ĐÀO TẠO</Tag>
      </div>
      <Alert
        showIcon
        type="info"
        message="Quy tắc kiểm tra lịch"
        description="Một phòng hoặc một giảng viên không được xuất hiện ở hai lớp trùng ngày, tiết và tuần học. Tiết học hợp lệ từ 1 đến 12."
        style={{ marginBottom: 18 }}
      />
      {error && (
        <Alert
          closable
          showIcon
          type="error"
          message={error}
          onClose={() => setError("")}
          style={{ marginBottom: 18 }}
        />
      )}
      <div className="admin-timetable-grid">
        <Card title="Danh sách lớp học phần" bodyStyle={{ padding: 0 }}>
          <Table
            rowKey="id"
            columns={columns}
            dataSource={assignments}
            pagination={{ pageSize: 10, hideOnSinglePage: true }}
            size="middle"
            rowClassName={(record) => (record.id === selected.id ? "ant-table-row-selected" : "")}
          />
        </Card>
        <Card title={"Điều chỉnh lớp " + selected.sectionCode}>
          <Form
            key={selected.id}
            className="admin-timetable-form"
            layout="vertical"
            initialValues={selected}
            onFinish={saveAssignment}
          >
            <Form.Item label="Giảng viên" name="lecturer">
              <Select options={lecturerOptions.map((value) => ({ value, label: value }))} />
            </Form.Item>
            <Form.Item label="Phòng máy / giảng đường" name="room">
              <Select options={roomOptions.map((value) => ({ value, label: value }))} />
            </Form.Item>
            <Form.Item label="Thứ" name="dayOfWeek">
              <Select options={dayOptions} />
            </Form.Item>
            <Space style={{ display: "flex" }} size={12}>
              <Form.Item label="Tiết bắt đầu" name="startPeriod" style={{ flex: 1 }}>
                <InputNumber min={1} max={12} style={{ width: "100%" }} />
              </Form.Item>
              <Form.Item label="Tiết kết thúc" name="endPeriod" style={{ flex: 1 }}>
                <InputNumber min={1} max={12} style={{ width: "100%" }} />
              </Form.Item>
            </Space>
            <Form.Item label="Tuần học" name="weeks">
              <Select
                options={[
                  { value: "1-15", label: "Tuần 1-15" },
                  { value: "1-8", label: "Tuần 1-8" },
                  { value: "9-15", label: "Tuần 9-15" },
                ]}
              />
            </Form.Item>
            <Space wrap style={{ marginBottom: 14 }}>
              <Tag color={lecturerConflicts.length ? "red" : "green"}>
                GV: {lecturerConflicts.length ? "Có xung đột" : "Không xung đột"}
              </Tag>
              <Tag color={roomConflicts.length ? "red" : "green"}>
                Phòng: {roomConflicts.length ? "Có xung đột" : "Không xung đột"}
              </Tag>
            </Space>
            <Button type="primary" htmlType="submit" block>
              Lưu phân công
            </Button>
          </Form>
        </Card>
      </div>
      <Alert
        type="warning"
        showIcon
        message="Dữ liệu giao diện mẫu"
        description="API timetable hiện chưa hoàn tất (backend đang trả 501), nên thao tác lưu được kiểm tra và cập nhật trong bộ nhớ trình duyệt."
        style={{ marginTop: 18 }}
      />
    </div>
  );
}
