export type Child = {
  id: string;
  name: string;
  grade: string;
  avatar: string;
  attendance: number;
  average: number;
  assignmentsDue: number;
  unreadMessages: number;
  alerts: string[];
  weeklySnapshot: string[];
};

export type TabId = "home" | "academics" | "attendance" | "messages" | "more";

export type TabItem = {
  id: TabId;
  label: string;
};

export type SubjectStat = {
  name: string;
  score: number;
  teacher: string;
};

export type AttendanceRecord = {
  label: string;
  status: "present" | "absent" | "late";
};

export type MessageThread = {
  title: string;
  unread: number;
  preview: string;
  lastUpdated: string;
  messages: MessageBubble[];
};

export type MessageBubble = {
  sender: "school" | "parent";
  body: string;
  time: string;
};

export type SubjectDetail = {
  name: string;
  teacher: string;
  currentAverage: number;
  recentTest: string;
  nextTask: string;
  progressNote: string;
  assignments: string[];
};

export type AttendanceDetail = {
  currentRate: number;
  presentDays: number;
  absentDays: number;
  lateDays: number;
  records: AttendanceRecord[];
  note: string;
};
