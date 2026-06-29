import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { colors, typography } from "../theme";

type Props = {
  label: string;
  value: string;
  tone?: "default" | "success" | "warning" | "danger";
};

export function StatTile({ label, value, tone = "default" }: Props) {
  return (
    <View style={[styles.tile, toneStyles[tone]]}>
      <View style={[styles.accentBar, accentStyles[tone]]} />
      <Text style={styles.value}>{value}</Text>
      <Text style={styles.label}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  tile: {
    flex: 1,
    borderRadius: 20,
    padding: 14,
    gap: 8,
    backgroundColor: colors.panelSoft,
    borderWidth: 1,
    borderColor: colors.border,
    overflow: "hidden",
    shadowColor: "#000",
    shadowOpacity: 0.18,
    shadowOffset: { width: 0, height: 8 },
    shadowRadius: 18,
    elevation: 4,
  },
  accentBar: {
    width: 28,
    height: 4,
    borderRadius: 999,
    marginBottom: 4,
  },
  value: {
    color: colors.text,
    fontSize: 24,
    fontFamily: typography.bold,
  },
  label: {
    color: colors.subtle,
    fontSize: 12,
  },
});

const toneStyles = StyleSheet.create({
  default: {
    backgroundColor: colors.panelSoft,
  },
  success: {
    borderColor: "rgba(91, 227, 127, 0.35)",
    backgroundColor: colors.successSoft,
  },
  warning: {
    borderColor: "rgba(246, 196, 83, 0.35)",
    backgroundColor: colors.warningSoft,
  },
  danger: {
    borderColor: "rgba(251, 129, 144, 0.35)",
    backgroundColor: colors.dangerSoft,
  },
});

const accentStyles = StyleSheet.create({
  default: {
    backgroundColor: colors.accent,
  },
  success: {
    backgroundColor: colors.success,
  },
  warning: {
    backgroundColor: colors.warning,
  },
  danger: {
    backgroundColor: colors.danger,
  },
});
