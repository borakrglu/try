import React from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
} from 'react-native';
import { useRouter } from 'expo-router';
import { COLORS, READING_TYPES } from '@/constants/config';

export default function ReadingsScreen() {
  const router = useRouter();

  const readingOptions = [
    { ...READING_TYPES.COFFEE, route: '/readings/coffee' },
    { ...READING_TYPES.TAROT, route: '/readings/tarot' },
    { ...READING_TYPES.PALM, route: '/readings/palm' },
    { ...READING_TYPES.ASTROLOGY, route: '/readings/astrology' },
  ];

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Choose Your Reading</Text>
      <Text style={styles.subtitle}>
        Select a mystical divination method to gain insights
      </Text>

      <View style={styles.grid}>
        {readingOptions.map((reading) => (
          <TouchableOpacity
            key={reading.id}
            style={styles.card}
            onPress={() => router.push(reading.route as any)}
          >
            <Text style={styles.emoji}>{reading.emoji}</Text>
            <Text style={styles.readingName}>{reading.name}</Text>
            <Text style={styles.readingDescription}>{reading.description}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    padding: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    marginBottom: 32,
  },
  grid: {
    gap: 16,
  },
  card: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  emoji: {
    fontSize: 64,
    marginBottom: 16,
  },
  readingName: {
    fontSize: 24,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 8,
  },
  readingDescription: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
});
