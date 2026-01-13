import axios, { AxiosInstance, AxiosError } from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_URL, API_TIMEOUT } from '@/constants/config';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      timeout: API_TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      async (config) => {
        const token = await AsyncStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor to handle token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest: any = error.config;

        // If token expired, try to refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const refreshToken = await AsyncStorage.getItem('refresh_token');
            if (refreshToken) {
              const response = await axios.post(`${API_URL}/api/v1/auth/refresh`, {
                refresh_token: refreshToken,
              });

              const { access_token, refresh_token: newRefreshToken } = response.data;
              await AsyncStorage.setItem('access_token', access_token);
              await AsyncStorage.setItem('refresh_token', newRefreshToken);

              originalRequest.headers.Authorization = `Bearer ${access_token}`;
              return this.client(originalRequest);
            }
          } catch (refreshError) {
            // Refresh failed, logout user
            await AsyncStorage.multiRemove(['access_token', 'refresh_token', 'user']);
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async register(data: {
    email: string;
    password: string;
    name: string;
    language: string;
  }) {
    const response = await this.client.post('/api/v1/auth/register', data);
    return response.data;
  }

  async login(email: string, password: string) {
    const response = await this.client.post('/api/v1/auth/login', {
      email,
      password,
    });
    return response.data;
  }

  async googleLogin(idToken: string) {
    const response = await this.client.post('/api/v1/auth/google-login', {
      id_token: idToken,
    });
    return response.data;
  }

  // Reading endpoints
  async getCoffeeReading(question: string) {
    const response = await this.client.post('/api/v1/readings/coffee', {
      question,
    });
    return response.data;
  }

  async getTarotReading(question: string, cards: string[]) {
    const response = await this.client.post('/api/v1/readings/tarot', {
      question,
      cards,
    });
    return response.data;
  }

  async getPalmReading(imageUri: string) {
    const formData = new FormData();
    formData.append('file', {
      uri: imageUri,
      type: 'image/jpeg',
      name: 'palm.jpg',
    } as any);

    const response = await this.client.post('/api/v1/readings/palm', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async getAstrologyReading(birthDate: string, birthTime: string, birthPlace: string) {
    const response = await this.client.post('/api/v1/readings/astrology', {
      birth_date: birthDate,
      birth_time: birthTime,
      birth_place: birthPlace,
    });
    return response.data;
  }

  async getReadings(skip = 0, limit = 20) {
    const response = await this.client.get('/api/v1/readings/', {
      params: { skip, limit },
    });
    return response.data;
  }

  // Chat endpoints
  async sendChatMessage(persona: string, content: string) {
    const response = await this.client.post('/api/v1/chat/message', {
      persona,
      content,
    });
    return response.data;
  }

  async getChatHistory(persona: string, limit = 50) {
    const response = await this.client.get('/api/v1/chat/history', {
      params: { persona, limit },
    });
    return response.data;
  }

  async clearChatHistory(persona?: string) {
    const response = await this.client.delete('/api/v1/chat/history', {
      params: persona ? { persona } : {},
    });
    return response.data;
  }

  // Journal endpoints
  async createJournalEntry(content: string, entryType = 'reflection', mood?: string) {
    const response = await this.client.post('/api/v1/journal/entries', {
      content,
      entry_type: entryType,
      mood,
    });
    return response.data;
  }

  async getJournalEntries(skip = 0, limit = 20) {
    const response = await this.client.get('/api/v1/journal/entries', {
      params: { skip, limit },
    });
    return response.data;
  }

  async getJournalInsights() {
    const response = await this.client.get('/api/v1/journal/insights');
    return response.data;
  }

  async getDailyAffirmation() {
    const response = await this.client.get('/api/v1/journal/affirmation');
    return response.data;
  }

  // Astrology endpoints
  async getCurrentMoonPhase() {
    const response = await this.client.get('/api/v1/astrology/moon/current');
    return response.data;
  }

  async getZodiacCompatibility(sign1: string, sign2: string) {
    const response = await this.client.get('/api/v1/astrology/zodiac/compatibility', {
      params: { sign1, sign2 },
    });
    return response.data;
  }

  // User profile
  async getProfile() {
    const response = await this.client.get('/api/v1/auth/me');
    return response.data;
  }
}

export const apiClient = new ApiClient();
