import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Alert,
  RefreshControl,
} from 'react-native';
import { apiClient } from '@/services/api';
import { COLORS } from '@/constants/config';

export default function JournalScreen() {
  const [content, setContent] = useState('');
  const [entries, setEntries] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [showNewEntry, setShowNewEntry] = useState(true);

  useEffect(() => {
    loadEntries();
  }, []);

  const loadEntries = async () => {
    try {
      const response = await apiClient.getJournalEntries(0, 10);
      setEntries(response);
    } catch (error) {
      console.error('Error loading entries:', error);
    } finally {
      setRefreshing(false);
    }
  };

  const handleSaveEntry = async () => {
    if (!content.trim()) {
      Alert.alert('Error', 'Please write something in your journal');
      return;
    }

    setLoading(true);
    try {
      await apiClient.createJournalEntry(content);
      setContent('');
      setShowNewEntry(false);
      loadEntries();
      Alert.alert('Success', 'Your journal entry has been saved with AI insights!');
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed to save entry');
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadEntries();
  };

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
      <Text style={styles.title}>✍️ Mystical Journal</Text>
      <Text style={styles.subtitle}>
        Pour your thoughts into the universe. AI will analyze your emotions and chakras.
      </Text>

      {showNewEntry ? (
        <View style={styles.newEntryCard}>
          <TextInput
            style={styles.textArea}
            placeholder="How are you feeling today? What's on your mind?"
            placeholderTextColor={COLORS.textSecondary}
            value={content}
            onChangeText={setContent}
            multiline
            numberOfLines={10}
            textAlignVertical="top"
          />

          <View style={styles.buttonRow}>
            <TouchableOpacity
              style={[styles.button, styles.secondaryButton]}
              onPress={() => {
                setShowNewEntry(false);
                setContent('');
              }}
            >
              <Text style={styles.secondaryButtonText}>Cancel</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.button}
              onPress={handleSaveEntry}
              disabled={loading}
            >
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.buttonText}>Save & Analyze</Text>
              )}
            </TouchableOpacity>
          </View>
        </View>
      ) : (
        <TouchableOpacity
          style={styles.newEntryButton}
          onPress={() => setShowNewEntry(true)}
        >
          <Text style={styles.newEntryButtonText}>+ New Entry</Text>
        </TouchableOpacity>
      )}

      {/* Past Entries */}
      <View style={styles.entriesSection}>
        <Text style={styles.sectionTitle}>Past Entries</Text>
        {entries.map((entry, index) => (
          <View key={entry.id} style={styles.entryCard}>
            <Text style={styles.entryDate}>
              {new Date(entry.created_at).toLocaleDateString('en-US', {
                month: 'long',
                day: 'numeric',
                year: 'numeric',
              })}
            </Text>
            <Text style={styles.entryContent} numberOfLines={3}>
              {entry.content}
            </Text>

            {entry.sentiment_analysis && (
              <View style={styles.sentimentRow}>
                <Text style={styles.sentimentLabel}>Mood:</Text>
                <Text style={styles.sentimentValue}>
                  {entry.sentiment_analysis.primary_emotion}
                </Text>
              </View>
            )}
          </View>
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
    marginBottom: 24,
    lineHeight: 24,
  },
  newEntryCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: 16,
    marginBottom: 24,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  textArea: {
    fontSize: 16,
    color: COLORS.text,
    minHeight: 200,
    marginBottom: 16,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: 12,
  },
  button: {
    flex: 1,
    backgroundColor: COLORS.primary,
    borderRadius: 12,
    padding: 14,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  secondaryButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: COLORS.primary,
  },
  secondaryButtonText: {
    color: COLORS.primary,
    fontSize: 16,
    fontWeight: '600',
  },
  newEntryButton: {
    backgroundColor: COLORS.primary,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    marginBottom: 24,
  },
  newEntryButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  entriesSection: {
    gap: 12,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 8,
  },
  entryCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  entryDate: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginBottom: 8,
  },
  entryContent: {
    fontSize: 16,
    color: COLORS.text,
    marginBottom: 12,
    lineHeight: 22,
  },
  sentimentRow: {
    flexDirection: 'row',
    gap: 8,
  },
  sentimentLabel: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  sentimentValue: {
    fontSize: 14,
    color: COLORS.primary,
    fontWeight: '600',
  },
});
