import React from "react";
import { Pressable } from "react-native";
import { StyleSheet, Text, View } from "react-native";
import { Child } from "../types";
import { colors, spacing, typography } from "../theme";
import { subjectStats } from "../data/mock";

type Props = {
  child: Child;
  onOpenSubject: (subjectName: string) => void;
};

export function AcademicsScreen({ child, onOpenSubject }: Props) {
  return (
    <View style={styles.screen}>
      <View style={styles.hero}>
        <Text style={styles.heroLabel}>Academic average</Text>
        <Text style={styles.heroValue}>{child.average}%</Text>
        <Text style={styles.heroNote}>Performance-first overview for {child.name.split(" ")[0]}.</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Subjects</Text>
        {subjectStats.map((subject) => (
          <Pressable key={subject.name} onPress={() => onOpenSubject(subject.name)} style={styles.subjectRow}>
            <View style={styles.subjectMeta}>
              <Text style={styles.subjectName}>{subject.name}</Text>
              <Text style={styles.subjectTeacher}>{subject.teacher}</Text>
            </View>
            <Text style={styles.subjectScore}>{subject.score}%</Text>
          </Pressable>
        ))}
      </View>

      <Text style={styles.link}>View deeper subject details</Text>
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
    gap: 6,
  },
  heroLabel: {
    color: colors.subtle,
    fontSize: 12,
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  heroValue: {
    color: colors.text,
    fontSize: 36,
    fontFamily: typography.bold,
  },
  heroNote: {
    color: colors.subtle,
    fontSize: 13,
    lineHeight: 18,
  },
  section: {
    gap: 10,
  },
  sectionTitle: {
    color: colors.text,
    fontSize: 16,
    fontFamily: typography.bold,
  },
  subjectRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 12,
    paddingHorizontal: 12,
    borderRadius: 16,
    backgroundColor: "rgba(255,255,255,0.02)",
    borderBottomWidth: 1,
    borderBottomColor: "rgba(255, 255, 255, 0.04)",
  },
  subjectMeta: {
    flex: 1,
    gap: 3,
  },
  subjectName: {
    color: colors.text,
    fontSize: 14,
    fontFamily: typography.medium,
  },
  subjectTeacher: {
    color: colors.subtle,
    fontSize: 12,
  },
  subjectScore: {
    color: colors.accentWarm,
    fontSize: 15,
    fontFamily: typography.bold,
  },
  link: {
    color: colors.accent,
    fontSize: 14,
    fontFamily: typography.medium,
    alignSelf: "flex-start",
  },
});
