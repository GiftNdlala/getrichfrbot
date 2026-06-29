import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { Child } from "../types";
import { colors, typography } from "../theme";

type Props = {
  child: Child;
};

export function MoreScreen({ child }: Props) {
  return (
    <View style={styles.screen}>
      <View style={styles.profileCard}>
        <Text style={styles.name}>{child.name}</Text>
        <Text style={styles.meta}>{child.grade}</Text>
        <Text style={styles.summary}>Profile, settings, and school-level actions live here.</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>More</Text>
        <View style={styles.optionCard}>
          <Text style={styles.option}>Profile</Text>
        </View>
        <View style={styles.optionCard}>
          <Text style={styles.option}>Settings</Text>
        </View>
        <View style={styles.optionCard}>
          <Text style={styles.option}>School notices</Text>
        </View>
        <View style={styles.optionCard}>
          <Text style={styles.option}>Logout</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    gap: 16,
  },
  profileCard: {
    padding: 18,
    borderRadius: 22,
    backgroundColor: colors.panelSoft,
    borderWidth: 1,
    borderColor: colors.border,
    gap: 4,
  },
  name: {
    color: colors.text,
    fontSize: 20,
    fontFamily: typography.bold,
  },
  meta: {
    color: colors.subtle,
    fontSize: 14,
  },
  summary: {
    color: colors.subtle,
    fontSize: 13,
    lineHeight: 18,
    marginTop: 6,
  },
  section: {
    gap: 10,
  },
  sectionTitle: {
    color: colors.text,
    fontSize: 16,
    fontFamily: typography.bold,
  },
  option: {
    color: colors.text,
    fontSize: 14,
    fontFamily: typography.medium,
  },
  optionCard: {
    padding: 14,
    borderRadius: 18,
    backgroundColor: colors.panelSoft,
    borderWidth: 1,
    borderColor: colors.border,
  },
});
