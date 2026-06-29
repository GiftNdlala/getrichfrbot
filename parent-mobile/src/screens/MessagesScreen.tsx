import React from "react";
import { Pressable } from "react-native";
import { StyleSheet, Text, View } from "react-native";
import { Child } from "../types";
import { messageThreads } from "../data/mock";
import { colors, typography } from "../theme";

type Props = {
  child: Child;
  onOpenThread: (threadTitle: string) => void;
};

export function MessagesScreen({ child, onOpenThread }: Props) {
  return (
    <View style={styles.screen}>
      <Text style={styles.summary}>{child.unreadMessages} unread conversations</Text>

      <View style={styles.section}>
        {messageThreads.map((thread) => (
          <Pressable key={thread.title} onPress={() => onOpenThread(thread.title)} style={styles.threadRow}>
            <View style={styles.threadHeader}>
              <Text style={styles.threadTitle}>{thread.title}</Text>
              {thread.unread > 0 ? <Text style={styles.badge}>{thread.unread} new</Text> : null}
            </View>
            <Text style={styles.threadPreview}>{thread.preview}</Text>
            <Text style={styles.threadMeta}>{thread.lastUpdated}</Text>
          </Pressable>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    gap: 16,
  },
  summary: {
    color: colors.subtle,
    fontSize: 14,
  },
  section: {
    gap: 10,
  },
  threadRow: {
    padding: 14,
    borderRadius: 18,
    backgroundColor: colors.panelSoft,
    borderWidth: 1,
    borderColor: colors.border,
    gap: 8,
  },
  threadHeader: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 8,
  },
  threadTitle: {
    color: colors.text,
    fontSize: 15,
    fontFamily: typography.bold,
  },
  badge: {
    color: colors.text,
    fontSize: 12,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 999,
    backgroundColor: colors.accentSoft,
  },
  threadPreview: {
    color: colors.subtle,
    fontSize: 13,
    lineHeight: 18,
  },
  threadMeta: {
    color: colors.muted,
    fontSize: 12,
  },
});
