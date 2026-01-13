# 🌟 Mystic.ai - Mobile App

AI-powered mystical guidance platform mobile application built with React Native and Expo.

## ✨ Features

- **Authentication** - Login and Register
- **Home Dashboard** - Daily affirmations and moon phase
- **Readings** - Coffee, Tarot, Palm, and Astrology readings
- **Chat** - Talk to 3 AI personas (Sage, Witch, Astrologer)
- **Journal** - AI-powered sentiment analysis and chakra scoring
- **Profile** - User settings and account management

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ installed
- npm or yarn
- Expo Go app on your phone ([iOS](https://apps.apple.com/app/expo-go/id982107779) | [Android](https://play.google.com/store/apps/details?id=host.exp.exponent))

### Installation

```bash
# Navigate to the app folder
cd mystic-ai-app

# Install dependencies
npm install

# Start the development server
npx expo start
```

### Testing on Your Phone

1. Install **Expo Go** app on your phone
2. Run `npx expo start`
3. Scan the QR code with your phone camera (iOS) or Expo Go app (Android)
4. App will load on your phone!

## ⚙️ Configuration

### Backend URL

Update the backend URL in `constants/config.ts`:

```typescript
export const API_URL = __DEV__ 
  ? 'http://localhost:8000'  // For local testing
  : 'https://your-backend.railway.app';  // For production
```

**Important:** If testing on a physical phone with local backend, use your computer's IP address:
```typescript
export const API_URL = 'http://192.168.1.XXX:8000'; // Replace with your IP
```

Find your IP:
- **Mac/Linux**: Run `ifconfig | grep "inet " | grep -v 127.0.0.1`
- **Windows**: Run `ipconfig` and look for IPv4 Address

## 📱 App Structure

```
mystic-ai-app/
├── app/
│   ├── (auth)/           # Authentication screens
│   │   ├── login.tsx
│   │   └── register.tsx
│   ├── (tabs)/           # Main app screens
│   │   ├── index.tsx     # Home
│   │   ├── readings.tsx
│   │   ├── chat.tsx
│   │   ├── journal.tsx
│   │   └── profile.tsx
│   ├── readings/         # Reading detail screens
│   │   ├── coffee.tsx
│   │   ├── tarot.tsx
│   │   ├── palm.tsx
│   │   └── astrology.tsx
│   └── _layout.tsx       # Root layout
├── components/           # Reusable components
├── context/             # React context (Auth)
├── services/            # API client
├── constants/           # Configuration
└── package.json
```

## 🔧 Development

### Running on Different Platforms

```bash
# iOS Simulator (Mac only)
npx expo start --ios

# Android Emulator
npx expo start --android

# Web Browser
npx expo start --web

# Physical Device (recommended)
npx expo start
# Then scan QR code
```

### Common Issues

**Issue: Can't connect to backend**
- Make sure backend is running
- Update API_URL with correct URL/IP
- Check firewall settings

**Issue: White screen on app**
- Check console for errors
- Restart Metro bundler: `npx expo start --clear`

**Issue: Module not found**
- Clear cache: `npx expo start --clear`
- Reinstall: `rm -rf node_modules && npm install`

## 📦 Building for Production

### iOS

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Build for iOS
eas build --platform ios
```

### Android

```bash
# Build APK
eas build --platform android --profile preview

# Build for Play Store
eas build --platform android
```

## 🎨 Customization

### Colors

Edit `constants/config.ts` to change app colors:

```typescript
export const COLORS = {
  primary: '#8B5CF6',      // Purple
  secondary: '#EC4899',    // Pink
  background: '#1a0033',   // Dark purple
  // ...
};
```

### Features

All features connect to your backend API. Make sure backend is deployed and accessible.

## 📄 License

Part of the Mystic.ai platform.

## 🆘 Support

For issues:
- Check the README
- Review console logs
- Make sure backend is running

---

**Built with React Native + Expo** 🚀
