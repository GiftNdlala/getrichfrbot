import React, { useMemo, useState } from "react";
import {
  Pressable,
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { ChildSwitcher } from "./src/components/ChildSwitcher";
import { ScreenCard } from "./src/components/ScreenCard";
import { mockChildren, tabs } from "./src/data/mock";
import { AcademicsScreen } from "./src/screens/AcademicsScreen";
import { AttendanceScreen } from "./src/screens/AttendanceScreen";
import { HomeScreen } from "./src/screens/HomeScreen";
import { MessagesScreen } from "./src/screens/MessagesScreen";
import { MoreScreen } from "./src/screens/MoreScreen";
import { AttendanceDetailScreen } from "./src/screens/AttendanceDetailScreen";
import { MessageThreadScreen } from "./src/screens/MessageThreadScreen";
import { SubjectDetailScreen } from "./src/screens/SubjectDetailScreen";
import { colors, spacing, typography } from "./src/theme";
import { TabId } from "./src/types";

type DetailRoute =
  | { type: "subject"; subjectName: string }
  | { type: "attendance" }
  | { type: "thread"; threadTitle: string };

const metricHighlights = [
  { label: "Average", value: "76%", tone: "accentWarm" as const },
  { label: "Attendance", value: "97%", tone: "success" as const },
  { label: "Due", value: "2", tone: "warning" as const },
  { label: "Unread", value: "1", tone: "accent" as const },
];

export default function App() {
  const [activeTab, setActiveTab] = useState<TabId>("home");
  const [detailRoute, setDetailRoute] = useState<DetailRoute | null>(null);
  const [activeChildId, setActiveChildId] = useState(mockChildren[0].id);

  const activeChild = useMemo(
    () => mockChildren.find((child) => child.id === activeChildId) ?? mockChildren[0],
    [activeChildId],
  );

  const activeTabLabel = tabs.find((tab) => tab.id === activeTab)?.label ?? "Home";
  const routeTitle = detailRoute
    ? detailRoute.type === "subject"
      ? detailRoute.subjectName
      : detailRoute.type === "attendance"
        ? "Attendance detail"
        : detailRoute.threadTitle
    : activeTabLabel;

  const openTab = (tab: TabId) => {
    setActiveTab(tab);
    setDetailRoute(null);
  };

  const openSubject = (subjectName: string) => {
    setActiveTab("academics");
    setDetailRoute({ type: "subject", subjectName });
  };

  const openAttendance = () => {
    setActiveTab("attendance");
    setDetailRoute({ type: "attendance" });
  };

  const openThread = (threadTitle: string) => {
    setActiveTab("messages");
    setDetailRoute({ type: "thread", threadTitle });
  };

  const goBack = () => setDetailRoute(null);

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="light-content" />
      <View style={styles.backgroundGlowOne} />
      <View style={styles.backgroundGlowTwo} />
      <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
        <View style={styles.hero}>
          <View style={styles.heroRow}>
            <View style={styles.heroText}>
              <Text style={styles.kicker}>Parent Portal</Text>
              <Text style={styles.title}>{detailRoute ? routeTitle : "Good morning, Mrs Ndlala"}</Text>
              <Text style={styles.subtitle}>
                {detailRoute
                  ? `${activeChild.name} · ${activeChild.grade}`
                  : "Child performance, attendance, and messages in one calm mobile view."}
              </Text>
            </View>
            <View style={styles.phasePill}>
              <Text style={styles.phasePillLabel}>Phase 1</Text>
            </View>
          </View>

          {!detailRoute ? (
            <View style={styles.metricsRow}>
              {metricHighlights.map((metric) => (
                <View key={metric.label} style={[styles.metricChip, metricToneStyles[metric.tone]]}>
                  <Text style={styles.metricValue}>{metric.value}</Text>
                  <Text style={styles.metricLabel}>{metric.label}</Text>
                </View>
              ))}
            </View>
          ) : (
            <Pressable onPress={goBack} style={({ pressed }) => [styles.backButton, pressed && styles.pressed]}>
              <Text style={styles.backButtonText}>Back to overview</Text>
            </Pressable>
          )}
        </View>

        <ChildSwitcher
          children={mockChildren}
          activeChildId={activeChildId}
          onChange={setActiveChildId}
        />

        <ScreenCard>
          {!detailRoute ? (
            <>
              {activeTab === "home" ? (
                <HomeScreen
                  child={activeChild}
                  onOpenAcademics={() => openTab("academics")}
                  onOpenAttendance={openAttendance}
                  onOpenMessages={() => openTab("messages")}
                />
              ) : null}
              {activeTab === "academics" ? (
                <AcademicsScreen child={activeChild} onOpenSubject={openSubject} />
              ) : null}
              {activeTab === "attendance" ? (
                <AttendanceScreen child={activeChild} onOpenDetails={openAttendance} />
              ) : null}
              {activeTab === "messages" ? (
                <MessagesScreen child={activeChild} onOpenThread={openThread} />
              ) : null}
              {activeTab === "more" ? <MoreScreen child={activeChild} /> : null}
            </>
          ) : detailRoute.type === "subject" ? (
            <SubjectDetailScreen subjectName={detailRoute.subjectName} />
          ) : detailRoute.type === "attendance" ? (
            <AttendanceDetailScreen />
          ) : (
            <MessageThreadScreen threadTitle={detailRoute.threadTitle} />
          )}
        </ScreenCard>
      </ScrollView>

      <View style={styles.tabBar}>
        {tabs.map((tab) => {
          const isActive = tab.id === activeTab && !detailRoute;

          return (
            <Pressable
              key={tab.id}
              onPress={() => openTab(tab.id)}
              style={({ pressed }) => [
                styles.tabButton,
                isActive && styles.tabButtonActive,
                pressed && styles.tabButtonPressed,
              ]}
            >
              <Text style={[styles.tabLabel, isActive && styles.tabLabelActive]}>{tab.label}</Text>
            </Pressable>
          );
        })}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: colors.bg,
  },
  backgroundGlowOne: {
    position: "absolute",
    top: -120,
    right: -80,
    width: 240,
    height: 240,
    borderRadius: 240,
    backgroundColor: "rgba(116, 201, 255, 0.12)",
  },
  backgroundGlowTwo: {
    position: "absolute",
    top: 240,
    left: -100,
    width: 200,
    height: 200,
    borderRadius: 200,
    backgroundColor: "rgba(255, 208, 138, 0.08)",
  },
  container: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.lg,
    paddingBottom: 120,
    gap: spacing.lg,
  },
  hero: {
    padding: 18,
    borderRadius: 28,
    backgroundColor: colors.panel,
    borderWidth: 1,
    borderColor: colors.border,
    gap: 16,
    shadowColor: "#000",
    shadowOpacity: 0.24,
    shadowOffset: { width: 0, height: 10 },
    shadowRadius: 20,
    elevation: 5,
  },
  heroRow: {
    flexDirection: "row",
    alignItems: "flex-start",
    justifyContent: "space-between",
    gap: 16,
  },
  heroText: {
    flex: 1,
    gap: 6,
  },
  kicker: {
    color: colors.accentWarm,
    fontSize: 12,
    letterSpacing: 1.4,
    textTransform: "uppercase",
    fontFamily: typography.medium,
  },
  title: {
    color: colors.text,
    fontSize: 28,
    lineHeight: 34,
    fontFamily: typography.bold,
  },
  subtitle: {
    color: colors.subtle,
    fontSize: 14,
    lineHeight: 20,
    maxWidth: 320,
  },
  phasePill: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 999,
    backgroundColor: colors.accentSoft,
    borderWidth: 1,
    borderColor: "rgba(116, 201, 255, 0.24)",
  },
  phasePillLabel: {
    color: colors.text,
    fontSize: 12,
    fontFamily: typography.medium,
  },
  metricsRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 10,
  },
  metricChip: {
    flexGrow: 1,
    flexBasis: "46%",
    padding: 14,
    borderRadius: 20,
    borderWidth: 1,
    gap: 4,
    backgroundColor: colors.panelSoft,
  },
  metricValue: {
    color: colors.text,
    fontSize: 22,
    fontFamily: typography.bold,
  },
  metricLabel: {
    color: colors.subtle,
    fontSize: 12,
  },
  tabBar: {
    position: "absolute",
    left: spacing.lg,
    right: spacing.lg,
    bottom: spacing.md,
    flexDirection: "row",
    gap: 8,
    padding: 8,
    borderRadius: 24,
    backgroundColor: "rgba(15, 28, 46, 0.96)",
    borderWidth: 1,
    borderColor: colors.border,
    shadowColor: "#000",
    shadowOpacity: 0.22,
    shadowOffset: { width: 0, height: 10 },
    shadowRadius: 22,
    elevation: 8,
  },
  tabButton: {
    flex: 1,
    paddingVertical: 12,
    alignItems: "center",
    borderRadius: 18,
  },
  tabButtonActive: {
    backgroundColor: colors.accentSoft,
  },
  tabButtonPressed: {
    opacity: 0.9,
  },
  tabLabel: {
    color: colors.subtle,
    fontSize: 12,
    fontFamily: typography.medium,
  },
  tabLabelActive: {
    color: colors.text,
  },
  backButton: {
    alignSelf: "flex-start",
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 16,
    backgroundColor: colors.panelSoft,
    borderWidth: 1,
    borderColor: colors.border,
  },
  backButtonText: {
    color: colors.text,
    fontSize: 13,
    fontFamily: typography.medium,
  },
  pressed: {
    opacity: 0.92,
  },
});

const metricToneStyles = StyleSheet.create({
  accent: {
    borderColor: "rgba(116, 201, 255, 0.22)",
    backgroundColor: colors.accentSoft,
  },
  accentWarm: {
    borderColor: "rgba(255, 208, 138, 0.22)",
    backgroundColor: colors.accentWarmSoft,
  },
  success: {
    borderColor: "rgba(91, 227, 127, 0.22)",
    backgroundColor: colors.successSoft,
  },
  warning: {
    borderColor: "rgba(246, 196, 83, 0.22)",
    backgroundColor: colors.warningSoft,
  },
});
