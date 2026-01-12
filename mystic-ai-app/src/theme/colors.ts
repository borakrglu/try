/**
 * Mystic.ai Color Palette
 * Dark-first design with mystical theme
 */

export const colors = {
  // Primary Colors
  primary: '#240046',           // Deep Purple (Mystic Night)
  gold: '#FFD700',              // Gold (Divine Light)
  midnightBlue: '#0A0E27',      // Midnight Blue (Cosmic Depth)

  // Secondary Colors
  mysticPurple: '#7209B7',      // Mystic Purple
  lavenderMist: '#B8A9D6',      // Lavender Mist
  celestialWhite: '#F8F7FF',    // Celestial White

  // Semantic Colors
  success: '#10B981',           // Emerald
  warning: '#F59E0B',           // Amber
  error: '#EF4444',             // Ruby
  info: '#3B82F6',              // Sapphire

  // Dark Mode (Primary)
  dark: {
    background: '#0A0E27',
    surface: '#1A1A2E',
    card: '#2A2A3E',
    textPrimary: '#F8F7FF',
    textSecondary: 'rgba(248, 247, 255, 0.7)',
    border: 'rgba(255, 255, 255, 0.1)',
    overlay: 'rgba(0, 0, 0, 0.5)',
  },

  // Light Mode (Secondary)
  light: {
    background: '#F8F7FF',
    surface: '#FFFFFF',
    card: '#F3F0FF',
    textPrimary: '#1A1A2E',
    textSecondary: 'rgba(26, 26, 46, 0.7)',
    border: 'rgba(0, 0, 0, 0.1)',
    overlay: 'rgba(0, 0, 0, 0.3)',
  },

  // Gradients (CSS gradient strings)
  gradients: {
    mystic: 'linear-gradient(135deg, #240046 0%, #7209B7 50%, #B8A9D6 100%)',
    cosmic: 'radial-gradient(circle, #0A0E27 0%, #240046 100%)',
    goldShimmer: 'linear-gradient(90deg, #FFD700 0%, #FFC700 50%, #FFD700 100%)',
    purple: 'linear-gradient(135deg, #7209B7 0%, #B8A9D6 100%)',
  },

  // Transparent overlays
  transparent: {
    black10: 'rgba(0, 0, 0, 0.1)',
    black20: 'rgba(0, 0, 0, 0.2)',
    black50: 'rgba(0, 0, 0, 0.5)',
    white10: 'rgba(255, 255, 255, 0.1)',
    white20: 'rgba(255, 255, 255, 0.2)',
    purple10: 'rgba(114, 9, 183, 0.1)',
    purple30: 'rgba(114, 9, 183, 0.3)',
  },
};

// Type-safe color access
export type ColorKey = keyof typeof colors;

// Helper function to get color by theme
export const getThemeColors = (isDark: boolean = true) => {
  return isDark ? colors.dark : colors.light;
};
