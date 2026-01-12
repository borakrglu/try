/**
 * Mystic.ai Spacing System
 * 8px base unit
 */

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
  xxxl: 64,
};

// Component-specific spacing
export const componentSpacing = {
  cardPadding: spacing.md,
  screenPadding: 20,
  sectionGap: spacing.lg,
  buttonPaddingVertical: 16,
  buttonPaddingHorizontal: 32,
  inputPaddingVertical: 12,
  inputPaddingHorizontal: 16,
  iconSize: {
    small: 20,
    medium: 24,
    large: 32,
    xlarge: 48,
  },
};

// Border radius
export const borderRadius = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  xxl: 24,
  full: 9999,
};

// Shadows
export const shadows = {
  small: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  medium: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 4,
  },
  large: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.2,
    shadowRadius: 16,
    elevation: 8,
  },
  purple: {
    shadowColor: '#7209B7',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 6,
  },
  gold: {
    shadowColor: '#FFD700',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 6,
  },
};

// Type-safe spacing access
export type SpacingKey = keyof typeof spacing;
