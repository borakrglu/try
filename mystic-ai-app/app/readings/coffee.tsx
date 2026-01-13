import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { apiClient } from '@/services/api';
import { COLORS } from '@/constants/config';

export default function CoffeeReadingScreen() {
  const [question, setQuestion] = useState('');
  const [reading, setReading] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleGetReading = async () => {
    if (!question.trim()) {
      Alert.alert('Error', 'Please enter a question');
      return;
    }

    setLoading(true);
    try {
      const response = await apiClient.getCoffeeReading(question);
      setReading(response);
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed to get reading');
    } finally {
      setLoading(false);
    }
  };

  const handleNewReading = () => {
    setReading(null);
    setQuestion('');
  };

  if (reading) {
    return (
      <ScrollView style={styles.container} contentContainerStyle={styles.content}>
        <Text style={styles.emoji}>☕</Text>
        <Text style={styles.title}>Your Coffee Reading</Text>

        <View style={styles.questionCard}>
          <Text style={styles.questionLabel}>Your Question:</Text>
          <Text style={styles.questionText}>{question}</Text>
        </View>

        <View style={styles.readingCard}>
          <Text style={styles.readingText}>{reading.interpretation}</Text>
        </View>

        {reading.symbols && reading.symbols.length > 0 && (
          <View style={styles.symbolsCard}>
            <Text style={styles.symbolsTitle}>Symbols Detected:</Text>
            {reading.symbols.map((symbol: any, index: number) => (
              <View key={index} style={styles.symbolItem}>
                <Text style={styles.symbolName}>{symbol.symbol}</Text>
                <Text style={styles.symbolMeaning}>{symbol.meaning}</Text>
              </View>
            ))}
          </View>
        )}

        <TouchableOpacity style={styles.button} onPress={handleNewReading}>
          <Text style={styles.buttonText}>New Reading</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, styles.secondaryButton]}
          onPress={() => router.back()}
        >
          <Text style={styles.secondaryButtonText}>Back to Readings</Text>
        </TouchableOpacity>
      </ScrollView>
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.emoji}>☕</Text>
      <Text style={styles.title}>Coffee Cup Reading</Text>
      <Text style={styles.subtitle}>
        Ask a question and receive mystical insights from the ancient art of coffee reading
      </Text>

      <View style={styles.form}>
        <TextInput
          style={styles.input}
          placeholder="What question weighs on your mind?"
          placeholderTextColor={COLORS.textSecondary}
          value={question}
          onChangeText={setQuestion}
          multiline
          numberOfLines={4}
          textAlignVertical="top"
        />

        <TouchableOpacity
          style={styles.button}
          onPress={handleGetReading}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Get Reading</Text>
          )}
        </TouchableOpacity>
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
  emoji: {
    fontSize: 64,
    textAlign: 'center',
    marginBottom: 16,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 32,
    lineHeight: 24,
  },
  form: {
    gap: 16,
  },
  input: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    color: COLORS.text,
    borderWidth: 1,
    borderColor: COLORS.border,
    minHeight: 120,
  },
  button: {
    backgroundColor: COLORS.primary,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  secondaryButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: COLORS.primary,
  },
  secondaryButtonText: {
    color: COLORS.primary,
    fontSize: 18,
    fontWeight: '600',
  },
  questionCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  questionLabel: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 8,
  },
  questionText: {
    fontSize: 16,
    color: COLORS.text,
    fontStyle: 'italic',
  },
  readingCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  readingText: {
    fontSize: 16,
    color: COLORS.text,
    lineHeight: 24,
  },
  symbolsCard: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  symbolsTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 16,
  },
  symbolItem: {
    marginBottom: 12,
  },
  symbolName: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.primary,
    marginBottom: 4,
  },
  symbolMeaning: {
    fontSize: 14,
    color: COLORS.textSecondary,
    lineHeight: 20,
  },
});
