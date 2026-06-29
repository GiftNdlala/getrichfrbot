import React from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { Child } from "../types";
import { colors, spacing, typography } from "../theme";

type Props = {
  children: Child[];
  activeChildId: string;
  onChange: (childId: string) => void;
};

export function ChildSwitcher({ children, activeChildId, onChange }: Props) {
  return (
    <View style={styles.wrapper}>
      {children.map((child) => {
        const active = child.id === activeChildId;

        return (
          <Pressable
            key={child.id}
            onPress={() => onChange(child.id)}
            style={({ pressed }) => [
              styles.chip,
              active && styles.chipActive,
              pressed && styles.chipPressed,
            ]}
          >
            <View style={[styles.avatar, active && styles.avatarActive]}>
              <Text style={styles.avatarLabel}>{child.avatar}</Text>
            </View>
            <View style={styles.textBlock}>
              <Text style={[styles.name, active && styles.nameActive]} numberOfLines={1}>
                {child.name}
              </Text>
              <Text style={styles.grade}>{child.grade}</Text>
            </View>
          </Pressable>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    flexDirection: "row",
    gap: spacing.sm,
  },
  chip: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    padding: 12,
    borderRadius: 22,
    backgroundColor: colors.panel,
    borderWidth: 1,
    borderColor: colors.border,
  },
  chipActive: {
    backgroundColor: colors.panelSoft,
    borderColor: colors.accent,
  },
  chipPressed: {
    opacity: 0.92,
  },
  avatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: "rgba(255, 255, 255, 0.04)",
    alignItems: "center",
    justifyContent: "center",
  },
  avatarActive: {
    backgroundColor: colors.accentSoft,
  },
  avatarLabel: {
    color: colors.subtle,
    fontFamily: typography.bold,
    fontSize: 12,
  },
  textBlock: {
    flex: 1,
  },
  name: {
    color: colors.text,
    fontSize: 14,
    fontFamily: typography.medium,
  },
  nameActive: {
    color: colors.text,
  },
  grade: {
    color: colors.subtle,
    fontSize: 12,
    marginTop: 2,
  },
});
