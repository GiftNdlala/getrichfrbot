import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { attendanceDetail } from "../data/mock";
import { colors, typography } from "../theme";

export function AttendanceDetailScreen() {
  return (
    <View style={styles.screen}>
      <View style={styles.hero}>
        <Text style={styles.label}>Attendance rate</Text>
        <Text style={styles.value}>{attendanceDetail.currentRate}%</Text>
        <Text style={styles.note}>{attendanceDetail.note}</Text>
      </View>

      <View style={styles.statsRow}>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{attendanceDetail.presentDays}</Text>
          <Text style={styles.statLabel}>Present days</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{attendanceDetail.absentDays}</Text>
          <Text style={styles.statLabel}>Absent days</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{attendanceDetail.lateDays}</Text>
          <Text style={styles.statLabel}>Late days</Text>
        </View>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Recent records</Text>
        {attendanceDetail.records.map((record) => (
          <View key={record.label} style={styles.recordRow}>
            <Text style={styles.recordLabel}>{record.label}</Text>
            <Text style={styles.recordValue}>{record.status}</Text>
          </View>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    gap: 14,
  },
  hero: {
    padding: 18,
    borderRadius: 22,
    backgroundColor: colors.panelSoft,
    borderWidth: 1,
    borderColor: colors.border,
    gap: 6,
  },
  label: {
    color: colors.subtle,
    fontSize: 12,
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  value: {
    color: colors.text,
    fontSize: 36,
    fontFamily: typography.bold,
  },
  note: {
    color: colors.subtle,
    fontSize: 14,
    lineHeight: 20,
  },
  statsRow: {
    flexDirection: "row",
    gap: 10,
  },
  statCard: {
    flex: 1,
    padding: 14,
    borderRadius: 18,
    backgroundColor: colors.panelSoft,
    borderWidth: 1,
    borderColor: colors.border,
    gap: 4,
  },
  statValue: {
    color: colors.text,
    fontSize: 22,
    fontFamily: typography.bold,
  },
  statLabel: {
    color: colors.subtle,
    fontSize: 12,
  },
  card: {
    padding: 16,
    borderRadius: 20,
    backgroundColor: colors.panelSoft,
    borderWidth: 1,
    borderColor: colors.border,
    gap: 8,
  },
  cardTitle: {
    color: colors.text,
    fontSize: 15,
    fontFamily: typography.bold,
  },
  recordRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(255,255,255,0.06)",
  },
  recordLabel: {
    color: colors.text,
    fontSize: 14,
  },
  recordValue: {
    color: colors.subtle,
    fontSize: 13,
    textTransform: "capitalize",
  },
});
