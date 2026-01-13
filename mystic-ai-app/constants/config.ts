// API Configuration
// IMPORTANT: Update this URL when you deploy your backend
export const API_URL = __DEV__ 
  ? 'http://localhost:8000'  // For local testing
  : 'https://your-backend.railway.app';  // For production

export const API_TIMEOUT = 30000; // 30 seconds

export const COLORS = {
  primary: '#8B5CF6',
  secondary: '#EC4899',
  background: '#1a0033',
  surface: '#2d1b4e',
  text: '#ffffff',
  textSecondary: '#a78bfa',
  border: '#4c2a85',
  success: '#10b981',
  error: '#ef4444',
  warning: '#f59e0b',
};

export const PERSONAS = {
  SAGE: {
    id: 'SAGE',
    name: 'The Sage',
    emoji: '🧙',
    description: 'Ancient wisdom and philosophical guidance',
    color: '#8B5CF6',
  },
  WITCH: {
    id: 'WITCH',
    name: 'The Witch',
    emoji: '🧹',
    description: 'Mystical insights and natural magic',
    color: '#EC4899',
  },
  ASTROLOGER: {
    id: 'ASTROLOGER',
    name: 'The Astrologer',
    emoji: '🔮',
    description: 'Cosmic guidance and celestial wisdom',
    color: '#06b6d4',
  },
};

export const READING_TYPES = {
  COFFEE: {
    id: 'coffee',
    name: 'Coffee Reading',
    emoji: '☕',
    description: 'Ancient coffee cup fortune telling',
  },
  TAROT: {
    id: 'tarot',
    name: 'Tarot Reading',
    emoji: '🃏',
    description: 'Mystical tarot card insights',
  },
  PALM: {
    id: 'palm',
    name: 'Palm Reading',
    emoji: '🤚',
    description: 'Discover your destiny in your palm',
  },
  ASTROLOGY: {
    id: 'astrology',
    name: 'Astrology',
    emoji: '⭐',
    description: 'Cosmic insights from the stars',
  },
};
