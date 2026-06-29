import React from "react";
import { Pressable } from "react-native";
import { StyleSheet, Text, View } from "react-native";
import { Child } from "../types";
import { attendanceRecords } from "../data/mock";
import { colors, typography } from "../theme";

type Props = {
  child: Child;
  onOpenDetails: () => void;
};

export function AttendanceScreen({ child, onOpenDetails }: Props) {
  return (
    <View style={styles.screen}>
      <View style={styles.hero}>
        <Text style={styles.heroLabel}>Current rate</Text>
        <Text style={styles.heroValue}>{child.attendance}%</Text>
        <View style={styles.statsRow}>
          <Text style={styles.stat}>Present: 103 days</Text>
          <Text style={styles.stat}>Absent: 3 days</Text>
          <Text style={styles.stat}>Late: 1 day</Text>
        </View>
      </View>

      <Pressable onPress={onOpenDetails} style={({ pressed }) => [styles.detailButton, pressed && styles.pressed]}>
        <Text style={styles.detailButtonText}>View attendance detail</Text>
      </Pressable>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Recent records</Text>
        {attendanceRecords.map((record) => (
          <View key={record.label} style={styles.recordRow}>
            <Text style={styles.recordStatus}>
              {record.status === "present" ? "V" : record.status === "late" ? "!" : "X"}
            </Text>
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
    gap: 18,
  },
  hero: {
    padding: 18,
    borderRadius: 22,
    backgroundColor: colors.panelSoft,
    borderWidth: 1,
    borderColor: colors.border,
    gap: 8,
  },
  heroLabel: {
    color: colors.subtle,
    fontSize: 12,
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  heroValue: {
    color: colors.text,
    fontSize: 34,
    fontFamily: typography.bold,
  },
  statsRow: {
    gap: 6,
  },
  detailButton: {
    paddingVertical: 12,
    paddingHorizontal: 14,
    borderRadius: 16,
    backgroundColor: colors.accentSoft,
    borderWidth: 1,
    borderColor: "rgba(116, 201, 255, 0.22)",
    alignSelf: "flex-start",
  },
  detailButtonText: {
    color: colors.text,
    fontSize: 13,
    fontFamily: typography.medium,
  },
  pressed: {
    opacity: 0.92,
  },
  stat: {
    color: colors.subtle,
    fontSize: 14,
  },
  section: {
    gap: 10,
  },
  sectionTitle: {
    color: colors.text,
    fontSize: 16,
    fontFamily: typography.bold,
  },
  recordRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(255, 255, 255, 0.06)",
  },
  recordStatus: {
    width: 20,
    color: colors.subtle,
    fontSize: 14,
    textAlign: "center",
  },
  recordLabel: {
    flex: 1,
    color: colors.text,
    fontSize: 14,
  },
  recordValue: {
    color: colors.subtle,
    fontSize: 13,
    textTransform: "capitalize",
  },
});
