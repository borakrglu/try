# 🚀 NASIL BAŞLATILIIR - Çok Basit!

## ADIM 1: Node.js Kur (5 dakika)

**Windows/Mac:**
1. Git: https://nodejs.org
2. "LTS" versiyonunu indir (sol taraftaki)
3. Kur (Next, Next, Next...)
4. Kontrol et - terminalde yaz:
```bash
node --version
```
Bir sayı görmeli (örn: v20.10.0)

## ADIM 2: Bağımlılıkları Yükle (2 dakika)

Terminal/Komut İstemi'nde:

```bash
# App klasörüne git
cd /home/user/try/mystic-ai-app

# Bağımlılıkları yükle
npm install
```

Bu 2-3 dakika sürer, bekle. Çok şey indirecek!

## ADIM 3: Backend URL'ini Ayarla (1 dakika)

**Dosya aç:** `constants/config.ts`

**Değiştir:**
```typescript
export const API_URL = 'http://192.168.1.XXX:8000';
// XXX yerine kendi bilgisayarının IP'sini yaz
```

**IP'ni nasıl bulursun:**

**Mac/Linux:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Windows:**
```bash
ipconfig
```
IPv4 Address: 192.168.1.XXX gibi bir şey göreceksin.

**VEYA** Backend Railway'de ise:
```typescript
export const API_URL = 'https://your-app.railway.app';
```

## ADIM 4: Backend'i Başlat (Eğer lokalde ise)

**Başka bir terminal aç**, backend klasöründe:

```bash
cd /home/user/try/mystic-ai-backend
docker compose up -d
```

Backend http://localhost:8000 veya http://192.168.1.XXX:8000 adresinde çalışacak.

## ADIM 5: Uygulamayı Başlat! (30 saniye)

App klasöründe:

```bash
npx expo start
```

**Göreceksin:**
- Bir QR kod
- Tuşlar: a (Android), i (iOS), w (Web)

## ADIM 6: Telefonunda Aç!

### iOS (iPhone):

1. **App Store'dan "Expo Go" indir**
2. Expo Go'yu aç
3. Terminaldeki QR kodu **Kamera** ile tarat
4. App açılacak! ✨

### Android:

1. **Play Store'dan "Expo Go" indir**
2. Expo Go'yu aç
3. "Scan QR Code" tıkla
4. Terminaldeki QR kodu tarat
5. App açılacak! ✨

### Web (Tarayıcıda test):

Terminal'de `w` tuşuna bas. Tarayıcıda açılır!

## 🎉 HAZIR!

Şimdi uygulamayı kullanabilirsin:

1. **Kayıt Ol** - Email ve şifre ile
2. **Login** - Giriş yap
3. **Home** - Günlük affirmation gör
4. **Readings** - Kahve falı dene!
5. **Chat** - Sage ile konuş
6. **Journal** - Günlük yaz

## 🆘 SORUN ÇÖZME

### "Cannot connect to backend" Hatası

1. Backend çalışıyor mu kontrol et:
   - Tarayıcıda aç: http://192.168.1.XXX:8000/health
   - "healthy" görmeli

2. IP doğru mu?
   - `constants/config.ts` dosyasını kontrol et

3. Firewall kapalı mı?
   - Windows: Firewall'u kapat veya port 8000'i aç

### "Metro bundler" Hatası

```bash
# Önbelleği temizle
npx expo start --clear
```

### "Module not found" Hatası

```bash
# Yeniden yükle
rm -rf node_modules
npm install
npx expo start
```

### App beyaz ekran

1. Terminal'de hata var mı bak
2. Backend'e bağlanıyor mu kontrol et
3. Expo'yu yeniden başlat: `npx expo start --clear`

## 📞 YARDIM

Bir sorun mu var?

1. Hata mesajını oku (terminalde kırmızı yazılar)
2. Backend çalışıyor mu kontrol et
3. README.md'ye bak
4. Google'a yaz: "expo [hata mesajı]"

---

**İYİ EĞLENCELER! ✨🔮**
