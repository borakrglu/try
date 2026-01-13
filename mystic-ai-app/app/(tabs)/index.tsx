import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { useRouter } from 'expo-router';
import { useAuth } from '@/context/AuthContext';
import { apiClient } from '@/services/api';
import { COLORS } from '@/constants/config';

export default function HomeScreen() {
  const { user } = useAuth();
  const router = useRouter();
  const [affirmation, setAffirmation] = useState<string>('');
  const [moonPhase, setMoonPhase] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [affirmationData, moonData] = await Promise.all([
        apiClient.getDailyAffirmation(),
        apiClient.getCurrentMoonPhase(),
      ]);

      setAffirmation(affirmationData.affirmation);
      setMoonPhase(moonData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good Morning';
    if (hour < 18) return 'Good Afternoon';
    return 'Good Evening';
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={onRefresh}
          tintColor={COLORS.primary}
        />
      }
    >
      {/* Greeting */}
      <View style={styles.greetingSection}>
        <Text style={styles.greeting}>{getGreeting()}, {user?.name}! ✨</Text>
        <Text style={styles.subGreeting}>What mystical wisdom do you seek today?</Text>
      </View>

      {/* Daily Affirmation */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>💫 Daily Affirmation</Text>
        <Text style={styles.affirmationText}>{affirmation}</Text>
      </View>

      {/* Moon Phase */}
      {moonPhase && (
        <View style={styles.card}>
          <Text style={styles.cardTitle}>🌙 Current Moon Phase</Text>
          <View style={styles.moonPhaseContent}>
            <Text style={styles.moonPhaseEmoji}>{moonPhase.phase_emoji}</Text>
            <View style={styles.moonPhaseInfo}>
              <Text style={styles.moonPhaseName}>{moonPhase.phase_name}</Text>
              <Text style={styles.moonPhaseText}>{moonPhase.meaning}</Text>
            </View>
          </View>
        </View>
      )}

      {/* Quick Actions */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Quick Access</Text>
        <View style={styles.quickActions}>
          <TouchableOpacity
            style={styles.actionCard}
            onPress={() => router.push('/readings/coffee')}
          >
            <Text style={styles.actionEmoji}>☕</Text>
            <Text style={styles.actionText}>Coffee Reading</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.actionCard}
            onPress={() => router.push('/readings/tarot')}
          >
            <Text style={styles.actionEmoji}>🃏</Text>
            <Text style={styles.actionText}>Tarot Cards</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.actionCard}
            onPress={() => router.push('/readings/palm')}
          >
            <Text style={styles.actionEmoji}>🤚</Text>
            <Text style={styles.actionText}>Palm Reading</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.actionCard}
            onPress={() => router.push('/(tabs)/chat')}
          >
            <Text style={styles.actionEmoji}>🧙</Text>
            <Text style={styles.actionText}>Chat with Sage</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
  },
  content: {
    padding: 20,
  },
  greetingSection: {
    marginBottom: 24,
  },
  greeting: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 4,
  },
  subGreeting: {
    fontSize: 16,
    color: COLORS.textSecondary,
  },
  card: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 12,
  },
  affirmationText: {
    fontSize: 16,
    color: COLORS.textSecondary,
    lineHeight: 24,
    fontStyle: 'italic',
  },
  moonPhaseContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
  },
  moonPhaseEmoji: {
    fontSize: 48,
  },
  moonPhaseInfo: {
    flex: 1,
  },
  moonPhaseName: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 4,
  },
  moonPhaseText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    lineHeight: 20,
  },
  section: {
    marginTop: 8,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 16,
  },
  quickActions: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  actionCard: {
    width: '48%',
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  actionEmoji: {
    fontSize: 40,
    marginBottom: 8,
  },
  actionText: {
    fontSize: 14,
    color: COLORS.text,
    textAlign: 'center',
    fontWeight: '500',
  },
});
