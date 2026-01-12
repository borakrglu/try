/**
 * Mystic.ai Theme System
 * Central export for all theme tokens
 */

export { colors, getThemeColors, type ColorKey } from './colors';
export { typography, fontWeights, type TypographyKey } from './typography';
export { spacing, componentSpacing, borderRadius, shadows, type SpacingKey } from './spacing';

// Animation timings
export const animations = {
  fast: 150,
  normal: 300,
  slow: 600,
  spring: {
    damping: 15,
    stiffness: 150,
  },
};

// Haptic feedback types
export const hapticTypes = {
  light: 'impactLight' as const,
  medium: 'impactMedium' as const,
  heavy: 'impactHeavy' as const,
  selection: 'selection' as const,
  notification: {
    success: 'notificationSuccess' as const,
    warning: 'notificationWarning' as const,
    error: 'notificationError' as const,
  },
};

// Complete theme object
export const theme = {
  colors,
  typography,
  spacing,
  componentSpacing,
  borderRadius,
  shadows,
  animations,
  hapticTypes,
};

export type Theme = typeof theme;

export default theme;
