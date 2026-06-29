import {
  AttendanceDetail,
  AttendanceRecord,
  Child,
  MessageThread,
  SubjectDetail,
  SubjectStat,
  TabItem,
} from "../types";

export const tabs: TabItem[] = [
  { id: "home", label: "Home" },
  { id: "academics", label: "Academics" },
  { id: "attendance", label: "Attendance" },
  { id: "messages", label: "Messages" },
  { id: "more", label: "More" },
];

export const mockChildren: Child[] = [
  {
    id: "ayanda",
    name: "Ayanda Ndlala",
    grade: "Grade 10A",
    avatar: "YN",
    attendance: 97,
    average: 76,
    assignmentsDue: 2,
    unreadMessages: 1,
    alerts: ["Maths assignment due tomorrow", "New school announcement"],
    weeklySnapshot: ["Attended 5/5 days", "Submitted 3 assignments", "Average improved by 2%"],
  },
  {
    id: "sipho",
    name: "Sipho Ndlala",
    grade: "Grade 7B",
    avatar: "SN",
    attendance: 92,
    average: 69,
    assignmentsDue: 1,
    unreadMessages: 2,
    alerts: ["Life Sciences worksheet overdue"],
    weeklySnapshot: ["Attended 4/5 days", "Submitted 1 assignment", "Average steady this week"],
  },
];

export const subjectStats: SubjectStat[] = [
  { name: "Mathematics", score: 81, teacher: "Mrs Khumalo" },
  { name: "English", score: 73, teacher: "Mr Jacobs" },
  { name: "Life Sciences", score: 78, teacher: "Ms Dlamini" },
  { name: "Physical Sci.", score: 69, teacher: "Mr Naidoo" },
];

export const attendanceRecords: AttendanceRecord[] = [
  { label: "Today", status: "present" },
  { label: "Yesterday", status: "present" },
  { label: "Monday", status: "absent" },
  { label: "Friday", status: "present" },
];

export const messageThreads: MessageThread[] = [
  {
    title: "Principal",
    unread: 2,
    preview: "Important update about upcoming term events.",
    lastUpdated: "Today, 08:14",
    messages: [
      { sender: "school", body: "Good morning parents. Please note the term briefing on Friday.", time: "08:14" },
      { sender: "parent", body: "Thanks for the update.", time: "08:19" },
    ],
  },
  {
    title: "Grade Head",
    unread: 1,
    preview: "Please review the recent attendance concern.",
    lastUpdated: "Yesterday, 16:40",
    messages: [
      { sender: "school", body: "Ayanda was absent on Monday. Please confirm if there was a valid reason.", time: "16:40" },
    ],
  },
  {
    title: "Mathematics Teacher",
    unread: 0,
    preview: "Assignment feedback has been shared.",
    lastUpdated: "Monday, 11:05",
    messages: [
      { sender: "school", body: "The latest algebra homework has been marked.", time: "11:05" },
      { sender: "school", body: "Ayanda scored 81% and showed strong improvement.", time: "11:06" },
    ],
  },
];

export const quickActions = [
  "Message Teacher",
  "View Timetable",
  "School Notices",
  "Report Card",
];

export const subjectDetails: SubjectDetail[] = [
  {
    name: "Mathematics",
    teacher: "Mrs Khumalo",
    currentAverage: 81,
    recentTest: "Algebra Test - 82%",
    nextTask: "Due tomorrow: Revision worksheet",
    progressNote: "Performance has improved steadily over the last three weeks.",
    assignments: ["Algebra Homework", "Quadratic Revision", "Graphs Practice"],
  },
  {
    name: "English",
    teacher: "Mr Jacobs",
    currentAverage: 73,
    recentTest: "Reading Comprehension - 75%",
    nextTask: "Essay draft due Friday",
    progressNote: "Writing is improving, but grammar accuracy still needs attention.",
    assignments: ["Essay Draft", "Vocabulary Practice"],
  },
  {
    name: "Life Sciences",
    teacher: "Ms Dlamini",
    currentAverage: 78,
    recentTest: "Cell Biology Test - 79%",
    nextTask: "Lab summary due Thursday",
    progressNote: "Consistent work, with strong scores in tests and class activities.",
    assignments: ["Lab Summary", "Worksheet Review"],
  },
  {
    name: "Physical Sci.",
    teacher: "Mr Naidoo",
    currentAverage: 69,
    recentTest: "Energy Systems - 68%",
    nextTask: "Problem set due Monday",
    progressNote: "Results are steady, but this subject needs a bit more focus.",
    assignments: ["Problem Set", "Formula Review"],
  },
];

export const attendanceDetail: AttendanceDetail = {
  currentRate: 97,
  presentDays: 103,
  absentDays: 3,
  lateDays: 1,
  records: attendanceRecords,
  note: "Attendance remains excellent this term, with one midweek absence to follow up.",
};
