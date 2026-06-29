import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { subjectDetails } from "../data/mock";
import { colors, typography } from "../theme";

type Props = {
  subjectName: string;
};

export function SubjectDetailScreen({ subjectName }: Props) {
  const detail = subjectDetails.find((item) => item.name === subjectName) ?? subjectDetails[0];

  return (
    <View style={styles.screen}>
      <View style={styles.hero}>
        <Text style={styles.subjectName}>{detail.name}</Text>
        <Text style={styles.teacher}>{detail.teacher}</Text>
        <Text style={styles.average}>{detail.currentAverage}%</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Current focus</Text>
        <Text style={styles.body}>{detail.progressNote}</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Recent test</Text>
        <Text style={styles.body}>{detail.recentTest}</Text>
        <Text style={styles.subBody}>{detail.nextTask}</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Assignments</Text>
        {detail.assignments.map((assignment) => (
          <Text key={assignment} style={styles.assignment}>
            {assignment}
          </Text>
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
    gap: 4,
  },
  subjectName: {
    color: colors.text,
    fontSize: 24,
    fontFamily: typography.bold,
  },
  teacher: {
    color: colors.subtle,
    fontSize: 13,
  },
  average: {
    color: colors.accentWarm,
    fontSize: 34,
    fontFamily: typography.bold,
    marginTop: 8,
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
  body: {
    color: colors.subtle,
    fontSize: 14,
    lineHeight: 20,
  },
  subBody: {
    color: colors.muted,
    fontSize: 13,
    lineHeight: 18,
  },
  assignment: {
    color: colors.text,
    fontSize: 14,
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(255,255,255,0.06)",
  },
});
