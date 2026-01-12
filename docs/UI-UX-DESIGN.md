# Mystic.ai - UI/UX Design Specifications

**Version:** 1.0
**Date:** January 12, 2026

---

## Design Philosophy

**Core Principles:**
- **Mystical yet Modern**: Ancient wisdom meets cutting-edge AI
- **Intuitive Flow**: Users achieve goals in 3 taps or less
- **Atmospheric**: Immersive mystical experience without clutter
- **Trustworthy**: Premium feel, professional execution
- **Accessible**: WCAG 2.1 AA compliance

---

## Color Palette

### Primary Colors
```
Deep Purple (Mystic Night)
- Hex: #240046
- RGB: 36, 0, 70
- Use: Primary brand, headers, CTAs

Gold (Divine Light)
- Hex: #FFD700
- RGB: 255, 215, 0
- Use: Accents, highlights, premium features

Midnight Blue (Cosmic Depth)
- Hex: #0A0E27
- RGB: 10, 14, 39
- Use: Backgrounds, dark mode primary
```

### Secondary Colors
```
Mystic Purple
- Hex: #7209B7
- RGB: 114, 9, 183
- Use: Interactive elements, gradients

Lavender Mist
- Hex: #B8A9D6
- RGB: 184, 169, 214
- Use: Text on dark, soft highlights

Celestial White
- Hex: #F8F7FF
- RGB: 248, 247, 255
- Use: Light mode background, text
```

### Semantic Colors
```
Success (Emerald)
- Hex: #10B981
- Use: Confirmations, positive feedback

Warning (Amber)
- Hex: #F59E0B
- Use: Alerts, important notices

Error (Ruby)
- Hex: #EF4444
- Use: Errors, destructive actions

Info (Sapphire)
- Hex: #3B82F6
- Use: Informational messages
```

### Gradients
```
Mystic Gradient (Primary)
- Linear: #240046 → #7209B7 → #B8A9D6
- Use: Hero sections, cards, overlays

Cosmic Gradient (Secondary)
- Radial: #0A0E27 → #240046
- Use: Backgrounds, modals

Gold Shimmer
- Linear: #FFD700 → #FFC700 → #FFD700
- Use: Premium badges, highlights
```

---

## Typography

### Font Families
```
Headings: Cinzel (Serif)
- Elegant, mystical, timeless
- Weights: 400 (Regular), 600 (SemiBold), 700 (Bold)
- Use: H1, H2, H3, reading titles

Body: Inter (Sans-serif)
- Clean, readable, modern
- Weights: 400 (Regular), 500 (Medium), 600 (SemiBold)
- Use: Body text, UI labels, descriptions

Accent: Cormorant Garamond (Serif)
- Graceful, mystical quotes
- Weights: 400 (Regular), 400 Italic
- Use: Affirmations, quotes, special text
```

### Type Scale
```
H1 (Hero): 32px / 38px line / Bold
H2 (Screen Title): 24px / 30px line / SemiBold
H3 (Section): 20px / 26px line / SemiBold
H4 (Card Title): 18px / 24px line / Medium
Body Large: 16px / 24px line / Regular
Body: 14px / 20px line / Regular
Caption: 12px / 16px line / Regular
Tiny: 10px / 14px line / Medium
```

---

## Spacing System

**8px Base Unit**
```
xs: 4px
sm: 8px
md: 16px
lg: 24px
xl: 32px
2xl: 48px
3xl: 64px
```

**Component Spacing**
```
Card padding: 16px (md)
Screen padding: 20px
Section gap: 24px (lg)
Button padding: 12px 24px
Input padding: 12px 16px
```

---

## Component Library

### Buttons

**Primary Button**
```
Background: Mystic Gradient
Text: White, 16px, SemiBold
Padding: 16px 32px
Border Radius: 12px
Shadow: 0px 4px 12px rgba(114, 9, 183, 0.3)
Tap Effect: Scale 0.95 + haptic

States:
- Default: Full gradient
- Pressed: Opacity 0.8 + scale
- Disabled: Opacity 0.4
```

**Secondary Button**
```
Background: Transparent
Border: 2px solid Gold
Text: Gold, 16px, SemiBold
Padding: 14px 30px
Border Radius: 12px

States:
- Default: Border only
- Pressed: Background Gold 10% opacity
- Disabled: Border gray, text gray
```

**Icon Button**
```
Size: 48px circle
Background: Purple 10% opacity
Icon: White, 24px
Tap Effect: Ripple + haptic
```

### Cards

**Reading Card**
```
Background: Gradient overlay on image
Border Radius: 16px
Padding: 20px
Shadow: 0px 8px 24px rgba(0, 0, 0, 0.15)
Aspect Ratio: 3:4 (portrait)

Content:
- Icon (top-left): 32px
- Title: H3, White
- Description: Body, White 80% opacity
- CTA: Primary button
```

**Glass Card (Glassmorphism)**
```
Background: rgba(255, 255, 255, 0.08)
Backdrop Filter: blur(20px)
Border: 1px solid rgba(255, 255, 255, 0.12)
Border Radius: 20px
Padding: 24px
```

### Inputs

**Text Input**
```
Background: Dark mode: #1A1A2E, Light: White
Border: 1px solid #3A3A52 (default)
Border Active: 2px solid Purple
Border Radius: 12px
Padding: 14px 16px
Font: 16px (prevents iOS zoom)

Placeholder: Gray 50% opacity
Error: Red border + error text below
```

**Search Input**
```
Icon: Left (magnifying glass), 20px
Background: Dark 15% opacity
Border: None
Border Radius: 24px (pill)
Padding: 12px 16px 12px 44px
```

### Modals

**Bottom Sheet**
```
Background: Dark: #1A1A2E, Light: White
Border Radius (top): 24px
Handle: 48px x 4px rounded, center-top
Padding: 24px
Shadow: 0px -4px 24px rgba(0, 0, 0, 0.2)

Animation: Slide up from bottom
Backdrop: Black 50% opacity
```

**Full Screen Modal**
```
Background: Gradient background
Header: Title + close button
Body: Scrollable content
Footer: Action buttons (sticky)

Animation: Fade + scale
```

### Lists

**Flat List (Readings History)**
```
Item Height: 120px
Separator: 1px line, gray 10%
Padding: 16px
Tap Effect: Scale 0.98 + haptic

Content:
- Thumbnail (left): 80px square
- Title: H4
- Date: Caption, gray
- Icon (right): Chevron, 20px
```

---

## Animations

### Timing Functions
```
Fast: 150ms ease-out (buttons, switches)
Normal: 300ms ease-in-out (cards, modals)
Slow: 600ms ease-in-out (page transitions)
Spring: spring(1, 80, 10) (interactive elements)
```

### Key Animations

**Page Transitions**
```
Enter: Fade in + slide up 20px, 300ms
Exit: Fade out + slide down 20px, 200ms
```

**Loading States**
```
Skeleton: Shimmer gradient left-to-right, 1.5s loop
Spinner: Rotate 360° + pulsing opacity, 2s loop
Coffee Swirl: Custom Lottie animation, 3s loop
```

**Success Feedback**
```
Check Mark: Scale from 0 → 1.2 → 1, 500ms
Confetti: Lottie animation, 2s once
Badge Unlock: Zoom + particle burst, 800ms
```

**Gesture Responses**
```
Pull to Refresh: Elastic resistance + spinner
Swipe to Delete: Slide + red background reveal
Long Press: Scale + haptic after 400ms
```

---

## Screen Designs

### Welcome Screen
```
Layout:
- Full-screen gradient background
- Animated stars (parallax)
- App logo (center): 120px
- Tagline: "Your AI Mystic Guide"
- 3 value props (icons + text)
- "Get Started" button (bottom)
- "Sign In" text button (below)

Animation: Logo fade + scale on load
```

### Home Screen
```
Header:
- Profile avatar (left): 40px circle
- Karma points (center): Gold number + icon
- Premium badge (right): Gold crown (if premium)

Hero Section:
- Greeting: "Good evening, Luna"
- Daily energy card: Glass card with transit info
- Background: Time-based gradient (dawn/day/dusk/night)

Reading Cards:
- Grid: 2 columns
- Cards: Coffee, Tarot, Palm, Chat
- Each: Icon, title, brief description

Quick Actions (Bottom):
- Floating Action Button: "Daily Card"
- Secondary: "Journal Entry"

Bottom Nav:
- 5 tabs: Home, Library, Journal, Chat, Profile
- Icons: 28px, active = Gold, inactive = Gray
- Active indicator: Gold dot below
```

### Camera Screen (Coffee Reading)
```
Layout:
- Full-screen camera preview
- Top: Step indicator "1/3" + close button
- Center: Overlay guide (cup outline)
- Bottom: Instruction text + capture button

Overlay:
- Semi-transparent white outline
- "Align cup interior with guide"
- Real-time detection: Green checkmark when aligned

Capture Button:
- 72px circle
- White border, purple center
- Tap: Flash animation + haptic

Captured Preview:
- Thumbnail appears bottom-right
- Retake option
```

### Reading Result Screen
```
Layout:
- Hero Image (top): User's photo with annotations
- Title: "Luna's Coffee Fortune"
- Date: Caption, gray
- Reading Sections: Expandable accordions
  - Past (collapsed by default)
  - Present (expanded)
  - Future (collapsed)
- Symbols List: Horizontal scroll, tappable
- Actions (bottom):
  - Audio narration button
  - Save to library
  - Share (styled card export)

Symbol Annotation:
- Tap symbol → Modal with meaning
- Highlight on image
- Zoom on image
```

### Chat Screen
```
Header:
- Persona selector (dropdown)
- Avatar changes based on persona

Message List:
- User messages: Right-aligned, purple bubble
- AI messages: Left-aligned, glass card
- Timestamp: Below message, caption
- Typing indicator: 3 dots animation

Input Bar (bottom):
- Text input: Expandable (1-4 lines)
- Send button: Gold circle with arrow
- Voice input button (left)

Persona Styles:
- Sage: Lotus icon, cool purple
- Witch: Cauldron icon, green accent
- Astrologer: Star icon, cosmic blue
```

### Journal Screen
```
Calendar View (top):
- Month view with mood dots
- Current day highlighted (gold ring)
- Streak counter (flame icon)

Entry Editor:
- Mood picker: 5 emoji buttons
- Text area: Expandable, placeholder prompts
- Voice-to-text button
- Tags: Chip selector (#work #love #health)
- Save button (bottom)

Insights Card:
- Chakra wheel visualization
- Energy level bar graph
- Affirmation of the day
```

### Subscription Screen
```
Header:
- Title: "Unlock Your Full Potential"
- Current tier indicator

Comparison Table:
- 3 columns: Free, Weekly, Monthly
- Row by row feature comparison
- Checkmarks (green) vs X (red)

Premium Cards:
- Weekly: $4.99/week card
- Monthly: $14.99/month card (BEST VALUE badge)
- Each: Price, features list, CTA button

Footer:
- "Start 7-Day Free Trial"
- Fine print: Terms, auto-renewal info
- "Restore Purchases" link
```

---

## Iconography

### Icon Style
```
Design: Rounded line icons (2px stroke)
Size: 24px default, 32px large, 20px small
Color: Adapts to context (white/purple/gold)

Custom Icons Needed:
- Coffee cup (with steam)
- Tarot cards (fanned)
- Open palm
- Mystical chat bubble
- Chakra symbols (7 unique)
- Zodiac signs (12)
- Moon phases (8)
- Karma flame
```

### Icon Library
```
Use: React Native Vector Icons
Sets:
- Feather (general UI)
- MaterialCommunityIcons (specific)
- Custom SVGs (mystical icons)
```

---

## Illustrations & Assets

### Lottie Animations
```
1. Loading_CoffeeSwirl.json (3s loop)
2. Loading_TarotShuffle.json (2s loop)
3. Success_StarBurst.json (1s once)
4. BadgeUnlock_Confetti.json (2s once)
5. Onboarding_MysticWelcome.json (4s once)
```

### Image Requirements
```
Tarot Deck Images:
- 78 cards (Major + Minor Arcana)
- Resolution: 800x1400px (portrait)
- Style: Mystic Dreams theme
- Format: WebP for web, PNG for app

Background Patterns:
- Starfield (seamless tile)
- Constellation lines
- Mandala patterns (subtle)

Icon Assets:
- App icon: 1024x1024px (rounded square)
- Splash screen: 2x, 3x resolutions
```

---

## Accessibility

### WCAG 2.1 AA Compliance

**Color Contrast**
```
Text on Dark Background:
- White on #240046: 14.2:1 ✓
- Gold on #240046: 7.8:1 ✓

Text on Light Background:
- Dark on #F8F7FF: 16.1:1 ✓

Interactive Elements:
- Minimum 44x44px tap targets
- 8px spacing between tappable items
```

**Screen Reader Support**
```
- All images have alt text
- Buttons have aria-labels
- Focus indicators visible
- Heading hierarchy (H1 → H2 → H3)
```

**Motion Sensitivity**
```
- Respect prefers-reduced-motion
- Disable animations if requested
- Offer "Calm Mode" in settings
```

**Font Scaling**
```
- Support iOS Dynamic Type
- Support Android font scaling
- Test up to 200% size
- Maintain layout integrity
```

---

## Dark Mode (Primary)

Mystic.ai is **dark-first** design. Light mode is secondary.

**Dark Mode Palette**
```
Background: #0A0E27
Surface: #1A1A2E
Card: #2A2A3E
Text Primary: #F8F7FF
Text Secondary: rgba(248, 247, 255, 0.7)
Border: rgba(255, 255, 255, 0.1)
```

**Light Mode Palette** (Optional)
```
Background: #F8F7FF
Surface: #FFFFFF
Card: #F3F0FF
Text Primary: #1A1A2E
Text Secondary: rgba(26, 26, 46, 0.7)
Border: rgba(0, 0, 0, 0.1)

Note: Gradients remain vibrant in light mode
```

---

## Haptic Feedback

```
Light: Selection, tab switch
Medium: Button press, card tap
Heavy: Success action, unlock
Notification: Error, warning
```

---

## Sound Design

### Sound Effects
```
1. Button_Tap.mp3 (50ms, subtle click)
2. Card_Flip.mp3 (300ms, mystical whoosh)
3. Reading_Complete.mp3 (800ms, chime)
4. Badge_Unlock.mp3 (1s, magical sparkle)
5. Error.mp3 (200ms, soft error tone)
```

### Background Music (Optional)
```
Ambient_Mystical_432Hz.mp3
- Volume: 10% (very subtle)
- Loop: Seamless
- User can disable in settings
```

---

## Responsive Design

### Breakpoints
```
Small Phone: 320px - 375px
Standard Phone: 375px - 414px
Large Phone: 414px - 480px
Tablet: 768px - 1024px
```

### Adaptive Layouts
```
Phone: Single column, bottom nav
Tablet: Two columns, side nav
iPad Pro: Three columns, side nav + detail
```

---

## Implementation Notes

### React Native Setup
```typescript
// theme/colors.ts
export const colors = {
  primary: '#240046',
  gold: '#FFD700',
  background: '#0A0E27',
  // ...
};

// theme/typography.ts
export const typography = {
  h1: {
    fontFamily: 'Cinzel-Bold',
    fontSize: 32,
    lineHeight: 38,
  },
  // ...
};

// theme/spacing.ts
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};
```

### Component Example
```typescript
import styled from 'styled-components/native';
import { colors, spacing, typography } from '@/theme';

export const PrimaryButton = styled.TouchableOpacity`
  background: linear-gradient(135deg, ${colors.primary} 0%, ${colors.mysticPurple} 100%);
  padding: ${spacing.md}px ${spacing.xl}px;
  border-radius: 12px;
  shadow-color: ${colors.mysticPurple};
  shadow-opacity: 0.3;
  shadow-radius: 12px;
  shadow-offset: 0px 4px;
`;

export const ButtonText = styled.Text`
  color: white;
  font-family: ${typography.button.fontFamily};
  font-size: ${typography.button.fontSize}px;
  text-align: center;
`;
```

---

## Design Deliverables Checklist

- [ ] Figma design system library
- [ ] All screen mockups (iOS + Android)
- [ ] Interactive prototype (clickable flows)
- [ ] Icon asset pack (SVG + PNG)
- [ ] Lottie animation files
- [ ] Tarot card image set
- [ ] Style guide PDF
- [ ] Developer handoff (Zeplin/Figma)

---

*Design by UX Team*
*Last updated: 2026-01-12*
