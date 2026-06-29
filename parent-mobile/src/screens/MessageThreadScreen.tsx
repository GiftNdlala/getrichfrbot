import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { messageThreads } from "../data/mock";
import { colors, typography } from "../theme";

type Props = {
  threadTitle: string;
};

export function MessageThreadScreen({ threadTitle }: Props) {
  const thread = messageThreads.find((item) => item.title === threadTitle) ?? messageThreads[0];

  return (
    <View style={styles.screen}>
      <View style={styles.hero}>
        <Text style={styles.title}>{thread.title}</Text>
        <Text style={styles.meta}>{thread.lastUpdated}</Text>
      </View>

      <View style={styles.thread}>
        {thread.messages.map((message, index) => (
          <View
            key={`${thread.title}-${index}-${message.time}`}
            style={[
              styles.bubble,
              message.sender === "parent" ? styles.parentBubble : styles.schoolBubble,
            ]}
          >
            <Text style={styles.bubbleText}>{message.body}</Text>
            <Text style={styles.bubbleMeta}>{message.time}</Text>
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
    gap: 4,
  },
  title: {
    color: colors.text,
    fontSize: 22,
    fontFamily: typography.bold,
  },
  meta: {
    color: colors.subtle,
    fontSize: 13,
  },
  thread: {
    gap: 10,
  },
  bubble: {
    maxWidth: "88%",
    padding: 14,
    borderRadius: 18,
    gap: 6,
    borderWidth: 1,
  },
  schoolBubble: {
    alignSelf: "flex-start",
    backgroundColor: "rgba(116, 201, 255, 0.12)",
    borderColor: "rgba(116, 201, 255, 0.18)",
  },
  parentBubble: {
    alignSelf: "flex-end",
    backgroundColor: "rgba(255, 208, 138, 0.14)",
    borderColor: "rgba(255, 208, 138, 0.18)",
  },
  bubbleText: {
    color: colors.text,
    fontSize: 14,
    lineHeight: 20,
  },
  bubbleMeta: {
    color: colors.subtle,
    fontSize: 11,
    alignSelf: "flex-end",
  },
});
