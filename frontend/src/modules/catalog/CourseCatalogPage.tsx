import { useMemo, useState } from "react";
import {
  BookOutlined,
  CalendarOutlined,
  CloseOutlined,
  InfoCircleOutlined,
  SearchOutlined,
} from "@ant-design/icons";
import { Button, Empty, Input, Modal, Select, Table, Tag, Typography } from "antd";
import type { ColumnsType } from "antd/es/table";

interface Course {
  code: string;
  name: string;
  credits: number;
  recommendedSemester: number;
  assessment: { process: number; final: number };
  prerequisites: string[];
  corequisites: string[];
  description: string;
  program: string;
}

export const COURSES_DATA = [
  // --- KHOA HỌC CƠ BẢN & TOÁN ---
  {
    id: "MI1111",
    name: "Giải tích I",
    credits: 4,
    tuitionCredits: 4,
    department: "KTTD",
    recommendedSemester: 1,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: [],
    corequisites: [],
    category: "Toán và Khoa học cơ bản",
    description: "Phép tính vi tích phân hàm một biến số, chuỗi số và chuỗi hàm."
  },
  {
    id: "MI1141",
    name: "Đại số",
    credits: 4,
    tuitionCredits: 4,
    department: "KTTD",
    recommendedSemester: 1,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: [],
    corequisites: [],
    category: "Toán và Khoa học cơ bản",
    description: "Đại số tuyến tính, ma trận, định thức, không gian véc-tơ, dạng toàn phương."
  },
  {
    id: "IT2000",
    name: "Nhập môn CNTT và TT",
    credits: 3,
    tuitionCredits: 3,
    department: "TCNTT",
    recommendedSemester: 1,
    assessment: { process: 0.4, final: 0.6 },
    prerequisites: [],
    corequisites: [],
    category: "Toán và Khoa học cơ bản",
    description: "Giới thiệu tổng quan về ngành Công nghệ thông tin và Truyền thông."
  },
  {
    id: "IT1108",
    name: "Nhập môn lập trình",
    credits: 4,
    tuitionCredits: 4,
    department: "TCNTT",
    recommendedSemester: 1,
    assessment: { process: 0.4, final: 0.6 },
    prerequisites: [],
    corequisites: [],
    category: "Toán và Khoa học cơ bản",
    description: "Kiến thức nền tảng về lập trình, kiểu dữ liệu, cấu trúc điều khiển và mảng trên C/C++."
  },
  {
    id: "MI1121",
    name: "Giải tích II",
    credits: 3,
    tuitionCredits: 3,
    department: "KTTD",
    recommendedSemester: 2,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["MI1111"],
    corequisites: [],
    category: "Toán và Khoa học cơ bản",
    description: "Phép tính vi phân và tích phân hàm nhiều biến số, tích phân đường và mặt."
  },
  {
    id: "IT3020",
    name: "Toán rời rạc",
    credits: 3,
    tuitionCredits: 3,
    department: "TCNTT",
    recommendedSemester: 2,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["MI1141"],
    corequisites: [],
    category: "Toán và Khoa học cơ bản",
    description: "Logic mệnh đề, tập hợp, quan hệ, lý thuyết đồ thị và bài toán đếm."
  },
  {
    id: "MI1131",
    name: "Giải tích III",
    credits: 3,
    tuitionCredits: 3,
    department: "KTTD",
    recommendedSemester: 3,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["MI1121"],
    corequisites: [],
    category: "Toán và Khoa học cơ bản",
    description: "Phương trình vi phân, chuỗi Fourier và biến đổi Laplace."
  },
  {
    id: "MI2020",
    name: "Xác suất thống kê",
    credits: 3,
    tuitionCredits: 3,
    department: "KTTD",
    recommendedSemester: 3,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["MI1111"],
    corequisites: [],
    category: "Toán và Khoa học cơ bản",
    description: "Lý thuyết xác suất biến ngẫu nhiên và các phương pháp thống kê toán ứng dụng."
  },
  {
    id: "PH1120",
    name: "Vật lý đại cương II",
    credits: 3,
    tuitionCredits: 3,
    department: "VVLKT",
    recommendedSemester: 3,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: [],
    corequisites: [],
    category: "Toán và Khoa học cơ bản",
    description: "Điện học, từ học và sóng điện từ."
  },
  {
    id: "MI3052",
    name: "Nhập môn các phương pháp tối ưu",
    credits: 2,
    tuitionCredits: 2,
    department: "KTTD",
    recommendedSemester: 3,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["MI1141", "MI1121"],
    corequisites: [],
    category: "Toán và Khoa học cơ bản",
    description: "Quy hoạch tuyến tính, bài toán đối ngẫu và các phương pháp tối ưu phi tuyến."
  },

  // --- CƠ SỞ VÀ CỐT LÕI NGÀNH ---
  {
    id: "IT2022",
    name: "Thống kê ứng dụng và quy hoạch thực nghiệm",
    credits: 3,
    tuitionCredits: 3,
    department: "TCNTT",
    recommendedSemester: 2,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["MI2020"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Ứng dụng các kiểm định thống kê và phân tích phương sai trong thực nghiệm CNTT."
  },
  {
    id: "IT3011",
    name: "Cấu trúc dữ liệu và thuật toán",
    credits: 2,
    tuitionCredits: 2,
    department: "TCNTT",
    recommendedSemester: 2,
    assessment: { process: 0.4, final: 0.6 },
    prerequisites: ["IT1108"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Các cấu trúc dữ liệu cơ bản (danh sách, cây, đồ thị) và thiết kế giải thuật cơ bản."
  },
  {
    id: "IT3030",
    name: "Kiến trúc máy tính",
    credits: 3,
    tuitionCredits: 3,
    department: "TCNTT",
    recommendedSemester: 3,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["IT2000"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Tổ chức CPU, bộ nhớ, vào/ra dữ liệu và tập lệnh hợp ngữ cơ bản."
  },
  {
    id: "IT3100",
    name: "Lập trình hướng đối tượng",
    credits: 2,
    tuitionCredits: 2,
    department: "TCNTT",
    recommendedSemester: 3,
    assessment: { process: 0.4, final: 0.6 },
    prerequisites: ["IT1108"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Các nguyên lý OOP: đóng gói, kế thừa, đa hình và trừu tượng qua Java/C++."
  },
  {
    id: "IT3040",
    name: "Kỹ thuật lập trình",
    credits: 2,
    tuitionCredits: 2,
    department: "TCNTT",
    recommendedSemester: 4,
    assessment: { process: 0.4, final: 0.6 },
    prerequisites: ["IT3011"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Kỹ thuật tối ưu hóa mã nguồn, đệ quy nâng cao, quay lui và quy hoạch động."
  },
  {
    id: "IT3070",
    name: "Nguyên lý hệ điều hành",
    credits: 3,
    tuitionCredits: 3,
    department: "TCNTT",
    recommendedSemester: 4,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["IT3030"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Quản lý tiến trình, bộ nhớ, luồng, đồng bộ hóa và hệ thống tập tin."
  },
  {
    id: "IT3080",
    name: "Mạng máy tính",
    credits: 3,
    tuitionCredits: 3,
    department: "TCNTT",
    recommendedSemester: 4,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["IT3030"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Mô hình OSI, TCP/IP, các giao thức định tuyến mạng và tầng ứng dụng."
  },
  {
    id: "IT3160",
    name: "Nhập môn Trí tuệ nhân tạo",
    credits: 3,
    tuitionCredits: 3,
    department: "TCNTT",
    recommendedSemester: 4,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["IT3011"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Tìm kiếm trạng thái, lý thuyết trò chơi, logic mờ và giới thiệu học máy."
  },
  {
    id: "IT3090",
    name: "Cơ sở dữ liệu",
    credits: 3,
    tuitionCredits: 3,
    department: "TCNTT",
    recommendedSemester: 5,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["IT3011"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Mô hình quan hệ, ngôn ngữ SQL, thiết kế lược đồ quan hệ và dạng chuẩn."
  },
  {
    id: "IT3170",
    name: "Thuật toán ứng dụng",
    credits: 2,
    tuitionCredits: 2,
    department: "TCNTT",
    recommendedSemester: 5,
    assessment: { process: 0.4, final: 0.6 },
    prerequisites: ["IT3011"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Ứng dụng các thuật toán nâng cao giải quyết bài toán thực tế và thi đấu lập trình."
  },
  {
    id: "IT3180",
    name: "Nhập môn công nghệ phần mềm",
    credits: 3,
    tuitionCredits: 3,
    department: "TCNTT",
    recommendedSemester: 5,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["IT3100"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Quy trình phát triển phần mềm, phân tích yêu cầu, mô hình Scrum/Agile."
  },
  {
    id: "IT3150",
    name: "Project I",
    credits: 2,
    tuitionCredits: 2,
    department: "TCNTT",
    recommendedSemester: 5,
    assessment: { process: 0.5, final: 0.5 },
    prerequisites: ["IT3100"],
    corequisites: ["IT3090"],
    category: "Cơ sở và cốt lõi ngành",
    description: "Đồ án thực hành xây dựng phần mềm cơ bản theo nhóm."
  },
  {
    id: "IT3190",
    name: "Nhập môn Học máy và khai phá dữ liệu",
    credits: 3,
    tuitionCredits: 3,
    department: "TCNTT",
    recommendedSemester: 5,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["MI2020", "IT3011"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Các mô hình hồi quy, phân lớp dữ liệu, gom cụm và đánh giá mô hình học máy."
  },
  {
    id: "IT4653",
    name: "Học sâu và ứng dụng",
    credits: 2,
    tuitionCredits: 2,
    department: "TCNTT",
    recommendedSemester: 6,
    assessment: { process: 0.4, final: 0.6 },
    prerequisites: ["IT3190"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Kiến trúc mạng nơ-ron sâu CNN, RNN, Transformer và ứng dụng trong thị giác/NLP."
  },
  {
    id: "IT3120",
    name: "Phân tích và thiết kế hệ thống",
    credits: 2,
    tuitionCredits: 2,
    department: "TCNTT",
    recommendedSemester: 6,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["IT3180"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Biểu đồ UML, mô hình hóa luồng dữ liệu và thiết kế kiến trúc chi tiết cho hệ thống."
  },
  {
    id: "IT4015",
    name: "Nhập môn an toàn thông tin",
    credits: 3,
    tuitionCredits: 3,
    department: "TCNTT",
    recommendedSemester: 6,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["IT3080"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Mã hóa đối xứng/bất đối xứng, chữ ký số và an ninh mạng máy tính."
  },
  {
    id: "IT3930",
    name: "Project II",
    credits: 2,
    tuitionCredits: 2,
    department: "TCNTT",
    recommendedSemester: 6,
    assessment: { process: 0.5, final: 0.5 },
    prerequisites: ["IT3150"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Đồ án chuyên ngành CNTT mức độ trung bình áp dụng công nghệ thực tế."
  },
  {
    id: "IT4991",
    name: "Thực tập kỹ thuật",
    credits: 2,
    tuitionCredits: 2,
    department: "TCNTT",
    recommendedSemester: 6,
    assessment: { process: 0.5, final: 0.5 },
    prerequisites: [],
    corequisites: [],
    category: "Thực tập",
    description: "Tham gia thực tập kỹ thuật tại doanh nghiệp CNTT tối thiểu 6-8 tuần."
  },
  {
    id: "IT3940",
    name: "Project III",
    credits: 3,
    tuitionCredits: 3,
    department: "TCNTT",
    recommendedSemester: 7,
    assessment: { process: 0.5, final: 0.5 },
    prerequisites: ["IT3930"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Đồ án chuyên sâu chuẩn bị hướng nghiên cứu cho đồ án tốt nghiệp."
  },
  {
    id: "IT4244",
    name: "Quản trị dự án CNTT",
    credits: 2,
    tuitionCredits: 2,
    department: "TCNTT",
    recommendedSemester: 8,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["IT3180"],
    corequisites: [],
    category: "Cơ sở và cốt lõi ngành",
    description: "Quản lý phạm vi, chi phí, rủi ro, tiến độ và nhân lực dự án phần mềm."
  },

  // --- LÝ LUẬN CHÍNH TRỊ & PHÁP LUẬT ---
  {
    id: "EM1170",
    name: "Pháp luật đại cương",
    credits: 2,
    tuitionCredits: 2,
    department: "KKTVQL",
    recommendedSemester: 2,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: [],
    corequisites: [],
    category: "Lý luận chính trị & Pháp luật",
    description: "Kiến thức cơ bản về nhà nước và pháp luật Việt Nam."
  },
  {
    id: "SSH1111",
    name: "Triết học Mác - Lênin",
    credits: 3,
    tuitionCredits: 3,
    department: "KML",
    recommendedSemester: 3,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: [],
    corequisites: [],
    category: "Lý luận chính trị & Pháp luật",
    description: "Chủ nghĩa duy vật biện chứng và duy vật lịch sử."
  },
  {
    id: "SSH1121",
    name: "Kinh tế chính trị Mác - Lênin",
    credits: 2,
    tuitionCredits: 2,
    department: "KML",
    recommendedSemester: 4,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["SSH1111"],
    corequisites: [],
    category: "Lý luận chính trị & Pháp luật",
    description: "Học thuyết giá trị, giá trị thặng dư và kinh tế thị trường định hướng XHCN."
  },
  {
    id: "SSH1131",
    name: "Chủ nghĩa xã hội khoa học",
    credits: 2,
    tuitionCredits: 2,
    department: "KML",
    recommendedSemester: 5,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["SSH1111"],
    corequisites: [],
    category: "Lý luận chính trị & Pháp luật",
    description: "Sứ mệnh lịch sử của giai cấp công nhân và thời kỳ quá độ lên CNXH."
  },
  {
    id: "SSH1141",
    name: "Lịch sử Đảng cộng sản Việt Nam",
    credits: 2,
    tuitionCredits: 2,
    department: "KML",
    recommendedSemester: 6,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["SSH1111"],
    corequisites: [],
    category: "Lý luận chính trị & Pháp luật",
    description: "Sự ra đời và sự lãnh đạo của Đảng Cộng sản Việt Nam qua các thời kỳ."
  },
  {
    id: "SSH1151",
    name: "Tư tưởng Hồ Chí Minh",
    credits: 2,
    tuitionCredits: 2,
    department: "KML",
    recommendedSemester: 7,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["SSH1111"],
    corequisites: [],
    category: "Lý luận chính trị & Pháp luật",
    description: "Hệ thống quan điểm của Chủ tịch Hồ Chí Minh về cách mạng Việt Nam."
  },

  // --- TỐT NGHIỆP ---
  {
    id: "IT4995",
    name: "Đồ án tốt nghiệp cử nhân",
    credits: 6,
    tuitionCredits: 6,
    department: "TCNTT",
    recommendedSemester: 8,
    assessment: { process: 0.3, final: 0.7 },
    prerequisites: ["IT3940"],
    corequisites: [],
    category: "Đồ án tốt nghiệp",
    description: "Đồ án khóa luận tốt nghiệp hệ cử nhân ngành Khoa học máy tính."
  }
];

const courses: Course[] = COURSES_DATA.map((course) => ({ code: course.id, name: course.name, credits: course.credits, recommendedSemester: course.recommendedSemester, assessment: { process: course.assessment.process * 100, final: course.assessment.final * 100 }, prerequisites: course.prerequisites, corequisites: course.corequisites, description: course.description, program: course.department })); const semesterOptions = [
  { value: "all", label: "Tất cả học kỳ" },
  ...Array.from(new Set(courses.map((course) => course.recommendedSemester))).sort().map((semester) => ({
    value: String(semester),
    label: `Kỳ ${semester}`,
  })),
];

function RequirementTags({ course }: { course: Course }) {
  if (!course.prerequisites.length && !course.corequisites.length) {
    return <span className="course-catalog-muted">Không có</span>;
  }

  return (
    <div className="course-catalog-requirements">
      {course.prerequisites.map((code) => <Tag color="volcano" key={`pre-${code}`}>TT {code}</Tag>)}
      {course.corequisites.map((code) => <Tag color="cyan" key={`co-${code}`}>SH {code}</Tag>)}
    </div>
  );
}

export default function CourseCatalogPage() {
  const [search, setSearch] = useState(""); const [program, setProgram] = useState("all");
  const [semester, setSemester] = useState("all");
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);

  const programOptions = ["TCNTT", "KTTD", "KML", "VVLKT", "KKTVQL"].map((value) => ({ value, label: value })); const filteredCourses = useMemo(() => {
    const normalizedSearch = search.trim().toLocaleLowerCase("vi-VN");
    return courses.filter((course) => {
      const matchesSearch = !normalizedSearch || `${course.code} ${course.name}`.toLocaleLowerCase("vi-VN").includes(normalizedSearch);
      const matchesSemester = semester === "all" || String(course.recommendedSemester) === semester;
      return matchesSearch && matchesSemester && (program === "all" || course.program === program);
    });
  }, [program, search, semester]);

  const columns: ColumnsType<Course> = [
    {
      title: "Mã HP",
      dataIndex: "code",
      key: "code",
      width: 112,
      render: (code: string) => <span className="course-catalog-code">{code}</span>,
    },
    {
      title: "Tên học phần",
      dataIndex: "name",
      key: "name",
      render: (name: string, course) => (
        <div className="course-catalog-name-cell">
          <strong>{name}</strong>
          <span>{course.program}</span>
        </div>
      ),
    },
    { title: "TC", dataIndex: "credits", key: "credits", width: 68, align: "center" },
    {
      title: "Kỳ học",
      dataIndex: "recommendedSemester",
      key: "recommendedSemester",
      width: 104,
      render: (value: number) => <Tag color="gold">Kỳ {value}</Tag>,
    },
    {
      title: "Điều kiện tiên quyết / song hành",
      key: "requirements",
      width: 330,
      render: (_, course) => <RequirementTags course={course} />,
    },
  ];

  return (
    <div className="course-catalog-page">
      <style>{`
        .course-catalog-page { color: #263238; }
        .course-catalog-intro { display: flex; justify-content: space-between; gap: 24px; align-items: flex-start; margin-bottom: 20px; }
        .course-catalog-eyebrow { color: #a6192e; font-size: 11px; font-weight: 700; letter-spacing: .14em; margin: 0 0 8px; }
        .course-catalog-heading { margin: 0 !important; color: #20272b !important; }
        .course-catalog-subtitle { color: #6c757d; margin: 8px 0 0; max-width: 700px; }
        .course-catalog-program { border-left: 3px solid #a6192e; color: #626b70; font-size: 12px; padding: 8px 0 8px 12px; white-space: nowrap; }
        .course-catalog-program strong { color: #263238; display: block; font-size: 13px; margin-top: 3px; }
        .course-catalog-toolbar { background: #fff; border: 1px solid #e2e5e7; display: flex; gap: 12px; padding: 14px; margin-bottom: 12px; }
        .course-catalog-search { max-width: 390px; }
        .course-catalog-semester { width: 180px; }
        .course-catalog-summary { align-items: center; color: #6c757d; display: flex; font-size: 12px; gap: 8px; margin: 0 0 8px; }
        .course-catalog-summary strong { color: #a6192e; }
        .course-catalog-table .ant-table { border: 1px solid #e2e5e7; border-radius: 2px; }
        .course-catalog-table .ant-table-thead > tr > th { background: #f5f6f7; color: #525b60; font-size: 11px; letter-spacing: .04em; text-transform: uppercase; }
        .course-catalog-table .ant-table-tbody > tr { cursor: pointer; }
        .course-catalog-table .ant-table-tbody > tr:hover > td { background: #fff8f8 !important; }
        .course-catalog-code { color: #a6192e; font-family: Consolas, monospace; font-weight: 700; }
        .course-catalog-name-cell { display: flex; flex-direction: column; gap: 3px; }
        .course-catalog-name-cell span, .course-catalog-muted { color: #8a9398; font-size: 12px; }
        .course-catalog-requirements { display: flex; flex-wrap: wrap; gap: 4px; }
        .course-catalog-requirements .ant-tag { font-family: Consolas, monospace; font-size: 11px; margin: 0; }
        .course-catalog-legend { display: flex; gap: 14px; margin-top: 10px; color: #798388; font-size: 11px; }
        .course-catalog-legend .ant-tag { margin: 0 4px 0 0; }
        .course-catalog-detail { border-top: 1px solid #edf0f1; margin-top: 4px; padding-top: 16px; }
        .course-catalog-detail-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 18px; }
        .course-catalog-detail-card { background: #f7f8f8; padding: 12px; }
        .course-catalog-detail-card span { color: #778187; display: block; font-size: 11px; margin-bottom: 5px; text-transform: uppercase; }
        .course-catalog-detail-card strong { color: #273238; font-size: 16px; }
        .course-catalog-weight { display: flex; gap: 8px; margin-top: 8px; }
        .course-catalog-weight span { border-radius: 3px; font-size: 12px; padding: 4px 8px; }
        .course-catalog-weight-process { background: #fff0f0; color: #a6192e; }
        .course-catalog-weight-final { background: #e8f7fa; color: #087f8c; }
        .course-catalog-description { color: #566168; line-height: 1.65; margin-bottom: 0; }
        @media (max-width: 640px) { .course-catalog-intro { flex-direction: column; gap: 12px; } .course-catalog-toolbar { flex-direction: column; } .course-catalog-search, .course-catalog-semester { max-width: none; width: 100%; } }
      `}</style>

      <div className="course-catalog-intro">
        <div>
          <p className="course-catalog-eyebrow">TRA CỨU HỌC VỤ · CTĐT</p>
          <Typography.Title className="course-catalog-heading" level={2}>Danh mục học phần</Typography.Title>
          <p className="course-catalog-subtitle">Tra cứu thông tin học phần, điều kiện tiên quyết và học phần song hành trong chương trình đào tạo.</p>
        </div>
        <div className="course-catalog-program"><span>CHƯƠNG TRÌNH ĐÀO TẠO: KHOA HỌC MÁY TÍNH - K2024</span></div>
      </div>

      <div className="course-catalog-toolbar">
        <Input
          allowClear
          className="course-catalog-search"
          aria-label="Tìm học phần"
          placeholder="Tìm theo mã hoặc tên học phần"
          prefix={<SearchOutlined />}
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
        <Select aria-label="Chọn Viện hoặc Khoa" className="course-catalog-program" value={program} options={[{ value: "all", label: "Tất cả Viện/Khoa" }, ...programOptions]} onChange={setProgram} /><Select aria-label="Chọn học kỳ" className="course-catalog-semester" value={semester} options={semesterOptions} onChange={setSemester} suffixIcon={<CalendarOutlined />} />
        <Button aria-label="Xóa bộ lọc" icon={<CloseOutlined />} onClick={() => { setSearch(""); setProgram("all"); setSemester("all"); }} disabled={!search && program === "all" && semester === "all"}>Xóa lọc</Button>
      </div>

      <div className="course-catalog-summary"><BookOutlined /> Hiển thị <strong>{filteredCourses.length}</strong> / {courses.length} học phần · Bấm vào một dòng để xem chi tiết</div>
      <div className="course-catalog-table">
        <Table<Course>
          rowKey="code"
          size="small"
          columns={columns}
          dataSource={filteredCourses}
          pagination={{ pageSize: 10, showSizeChanger: false, showTotal: (total) => `Tổng ${total} học phần` }}
          locale={{ emptyText: <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description="Không tìm thấy học phần phù hợp." /> }}
          scroll={{ x: 760 }}
          onRow={(course) => ({ onClick: () => setSelectedCourse(course) })}
        />
      </div>
      <div className="course-catalog-legend"><span><Tag color="volcano">TT</Tag> Tiên quyết</span><span><Tag color="cyan">SH</Tag> Song hành</span><span><InfoCircleOutlined /> Thông tin được cập nhật theo CTĐT mẫu</span></div>

      <Modal open={selectedCourse !== null} onCancel={() => setSelectedCourse(null)} footer={null} title={selectedCourse ? `${selectedCourse.code} · ${selectedCourse.name}` : undefined} width={620}>
        {selectedCourse && (
          <div className="course-catalog-detail">
            <div className="course-catalog-detail-grid">
              <div className="course-catalog-detail-card"><span>Số tín chỉ</span><strong>{selectedCourse.credits} tín chỉ</strong></div>
              <div className="course-catalog-detail-card"><span>Kỳ khuyến nghị</span><strong>Kỳ {selectedCourse.recommendedSemester}</strong></div>
            </div>
            <Typography.Text strong>Tỷ lệ điểm</Typography.Text>
            <div className="course-catalog-weight"><span className="course-catalog-weight-process">Quá trình {selectedCourse.assessment.process}%</span><span className="course-catalog-weight-final">Cuối kỳ {selectedCourse.assessment.final}%</span></div>
            <Typography.Paragraph className="course-catalog-description" style={{ marginTop: 20 }}><Typography.Text strong>Mô tả học phần: </Typography.Text>{selectedCourse.description}</Typography.Paragraph>
            <Typography.Text strong>Các môn bắt buộc phải học trước</Typography.Text>
            <div className="course-catalog-requirements" style={{ marginTop: 8 }}><RequirementTags course={selectedCourse} /></div>
          </div>
        )}
      </Modal>
    </div>
  );
}
