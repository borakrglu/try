/**
 * Mystic.ai Typography System
 */

export const typography = {
  // Font Families
  fonts: {
    heading: 'Cinzel-Bold',          // Mystical serif for headings
    headingRegular: 'Cinzel-Regular',
    body: 'Inter-Regular',            // Clean sans-serif for body
    bodyMedium: 'Inter-Medium',
    bodySemiBold: 'Inter-SemiBold',
    accent: 'CormorantGaramond-Regular', // Graceful serif for quotes
    accentItalic: 'CormorantGaramond-Italic',
  },

  // Type Scale
  h1: {
    fontFamily: 'Cinzel-Bold',
    fontSize: 32,
    lineHeight: 38,
    letterSpacing: -0.5,
  },
  h2: {
    fontFamily: 'Cinzel-SemiBold',
    fontSize: 24,
    lineHeight: 30,
    letterSpacing: -0.3,
  },
  h3: {
    fontFamily: 'Cinzel-SemiBold',
    fontSize: 20,
    lineHeight: 26,
    letterSpacing: -0.2,
  },
  h4: {
    fontFamily: 'Inter-Medium',
    fontSize: 18,
    lineHeight: 24,
    letterSpacing: 0,
  },
  bodyLarge: {
    fontFamily: 'Inter-Regular',
    fontSize: 16,
    lineHeight: 24,
    letterSpacing: 0,
  },
  body: {
    fontFamily: 'Inter-Regular',
    fontSize: 14,
    lineHeight: 20,
    letterSpacing: 0,
  },
  caption: {
    fontFamily: 'Inter-Regular',
    fontSize: 12,
    lineHeight: 16,
    letterSpacing: 0.2,
  },
  tiny: {
    fontFamily: 'Inter-Medium',
    fontSize: 10,
    lineHeight: 14,
    letterSpacing: 0.3,
  },
  button: {
    fontFamily: 'Inter-SemiBold',
    fontSize: 16,
    lineHeight: 24,
    letterSpacing: 0.5,
  },
  quote: {
    fontFamily: 'CormorantGaramond-Italic',
    fontSize: 18,
    lineHeight: 26,
    letterSpacing: 0,
  },
};

// Font weights
export const fontWeights = {
  regular: '400' as const,
  medium: '500' as const,
  semiBold: '600' as const,
  bold: '700' as const,
};

// Type-safe typography access
export type TypographyKey = keyof typeof typography;
