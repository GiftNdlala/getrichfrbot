import React from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { StatTile } from "../components/StatTile";
import { quickActions } from "../data/mock";
import { Child } from "../types";
import { colors, spacing, typography } from "../theme";

type Props = {
  child: Child;
  onOpenAcademics: () => void;
  onOpenAttendance: () => void;
  onOpenMessages: () => void;
};

export function HomeScreen({ child, onOpenAcademics, onOpenAttendance, onOpenMessages }: Props) {
  return (
    <View style={styles.screen}>
      <View style={styles.heroStrip}>
        <Text style={styles.heroStripLabel}>Active child</Text>
        <Text style={styles.heroStripName}>{child.name}</Text>
        <Text style={styles.heroStripMeta}>{child.grade}</Text>
      </View>

      <View style={styles.alertCard}>
        <Text style={styles.alertTitle}>Needs attention</Text>
        {child.alerts.map((alert) => (
          <Text key={alert} style={styles.alertItem}>
            {alert}
          </Text>
        ))}
        <Pressable onPress={onOpenAttendance} style={({ pressed }) => [styles.inlineButton, pressed && styles.actionPressed]}>
          <Text style={styles.inlineButtonText}>View attendance detail</Text>
        </Pressable>
      </View>

      <View style={styles.grid}>
        <StatTile label="Average" value={`${child.average}%`} tone="default" />
        <StatTile label="Attendance" value={`${child.attendance}%`} tone="success" />
      </View>

      <View style={styles.grid}>
        <StatTile label="Assignments Due" value={String(child.assignmentsDue)} tone="warning" />
        <StatTile label="Messages" value={String(child.unreadMessages)} tone="default" />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Quick actions</Text>
        <View style={styles.actions}>
          {quickActions.map((action) => (
            <Pressable
              key={action}
              onPress={() => {
                if (action === "View Timetable") {
                  onOpenAcademics();
                }
                if (action === "Message Teacher") {
                  onOpenMessages();
                }
                if (action === "School Notices") {
                  onOpenMessages();
                }
                if (action === "Report Card") {
                  onOpenAcademics();
                }
              }}
              style={({ pressed }) => [styles.actionButton, pressed && styles.actionPressed]}
            >
              <Text style={styles.actionText}>{action}</Text>
            </Pressable>
          ))}
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>This week</Text>
        {child.weeklySnapshot.map((item) => (
          <Text key={item} style={styles.snapshotItem}>
            {item}
          </Text>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    gap: 16,
  },
  alertCard: {
    padding: 16,
    borderRadius: 20,
    backgroundColor: "rgba(251, 129, 144, 0.12)",
    borderWidth: 1,
    borderColor: "rgba(251, 129, 144, 0.22)",
    gap: 8,
  },
  alertTitle: {
    color: colors.text,
    fontSize: 15,
    fontFamily: typography.bold,
  },
  alertItem: {
    color: colors.subtle,
    fontSize: 14,
    lineHeight: 20,
  },
  heroStrip: {
    padding: 16,
    borderRadius: 20,
    backgroundColor: colors.panelSoft,
    borderWidth: 1,
    borderColor: colors.border,
    gap: 4,
  },
  heroStripLabel: {
    color: colors.accentWarm,
    fontSize: 12,
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  heroStripName: {
    color: colors.text,
    fontSize: 18,
    fontFamily: typography.bold,
  },
  heroStripMeta: {
    color: colors.subtle,
    fontSize: 13,
  },
  grid: {
    flexDirection: "row",
    gap: spacing.sm,
  },
  section: {
    gap: 8,
  },
  actions: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.sm,
  },
  actionButton: {
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderRadius: 999,
    backgroundColor: colors.panelSoft,
    borderWidth: 1,
    borderColor: colors.border,
  },
  actionPressed: {
    opacity: 0.9,
  },
  inlineButton: {
    marginTop: 4,
    alignSelf: "flex-start",
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderRadius: 999,
    backgroundColor: colors.panelSoft,
    borderWidth: 1,
    borderColor: colors.border,
  },
  inlineButtonText: {
    color: colors.text,
    fontSize: 12,
    fontFamily: typography.medium,
  },
  actionText: {
    color: colors.text,
    fontSize: 12,
    fontFamily: typography.medium,
  },
  sectionTitle: {
    color: colors.text,
    fontSize: 16,
    fontFamily: typography.bold,
  },
  snapshotItem: {
    color: colors.subtle,
    fontSize: 14,
    lineHeight: 20,
  },
});
