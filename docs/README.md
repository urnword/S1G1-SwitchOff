# 📖 Documentation — Switch Off!!!

Full project documentation, architecture details, and deployment guide.

---

## 📁 Contents

```
docs/
├── README.md       ← This file
├── report.pdf      ← Official project report
└── media/
    ├── dashboard.png      ← Web dashboard screenshot
    ├── prototype.jpg      ← Physical prototype photos
    ├── circuit_diagram.png
    └── demo.mp4           ← Presentation video
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER LAYER                          │
│                  Next.js Web Dashboard                      │
│         (Real-time monitoring + manual control)             │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTPS / Firestore SDK
┌─────────────────────────▼───────────────────────────────────┐
│                       CLOUD LAYER                           │
│                  Google Firebase                            │
│         Firestore (device state, commands, config)          │
│         Firebase Hosting (web app)                          │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP REST (urequests)
┌─────────────────────────▼───────────────────────────────────┐
│                      DEVICE LAYER                           │
│              ESP32 NodeMCU (MicroPython)                    │
│                                                             │
│  Inputs:                        Outputs:                    │
│  • HLK-LD2410C (mmWave)         • L298N → N20 Motor        │
│  • GL55 LDR (light)             • LED indicators           │
│  • KY-037 Sound (fan)           • Buzzer                   │
└─────────────────────────────────────────────────────────────┘
                          │ Physical
┌─────────────────────────▼───────────────────────────────────┐
│                    PHYSICAL LAYER                           │
│         Rack & Pinion → Metal Shaft → Wall Switch          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 System Flowchart

### Main Loop (ESP32)

```
START
  │
  ▼
Initialize: Wi-Fi connect, sensor calibration
  │
  ▼
┌─────────────────────┐
│   READ SENSOR DATA  │ ◄────────────────────────┐
└────────┬────────────┘                           │
         │                                        │
         ▼                                        │
   HUMAN DETECTED?                                │
   YES ──► Motor OFF, keep devices on             │
   NO  ──► Check: LIGHT or FAN ON?                │
              YES ──► Start auto-off timer         │
                      Timer expired? ──► Motor ON │
              NO  ──► All good, no action          │
         │                                        │
         ▼                                        │
   CHECK CLOUD COMMANDS                           │
   (runMotor, config changes)                     │
         │                                        │
         ▼                                        │
   SEND STATUS TO FIRESTORE ─────────────────────┘
   (only on state change)
```

### Data Flow (Cloud)

```
ESP32 ──PATCH──► Firestore (status update)
                      │
                      ▼ real-time listener
              Next.js Dashboard (display)

User clicks "Turn Off"
       │
       ▼
Next.js ──WRITE──► Firestore (command: runMotor=true)
                        │
                        ▼ ESP32 polls every 200ms
                   ESP32 reads command ──► activates motor
                   ESP32 marks command executed=true
```

---

## 🌐 Web Dashboard

**Live:** [https://studio--switch-off-b68c4.us-central1.hosted.app/](https://studio--switch-off-b68c4.us-central1.hosted.app/)

### Features
- **Device overview** — list of registered Switch Off!!! devices
- **Real-time status** — Presence / Light / Fan / Switch state updated live
- **Manual control** — Turn On / Turn Off buttons send commands to the device
- **Device configuration** — Toggle Auto-Off, set delay duration
- **Last seen timestamp** — Know when the device last checked in

### Local Development

```bash
# Clone repo
git clone https://github.com/urnword/switch-off.git
cd switch-off/web

# Install dependencies
npm install

# Add your Firebase config
cp .env.example .env.local
# Fill in your Firebase project credentials in .env.local

# Run dev server
npm run dev
# Open http://localhost:3000
```

### Firebase Setup

1. Create a Firebase project at [console.firebase.google.com](https://console.firebase.google.com)
2. Enable **Firestore Database** (start in test mode for development)
3. Enable **Firebase Hosting**
4. Copy your Firebase config into `.env.local`

**Firestore Document Structure:**
```
devices/
  {deviceId}/
    fields:
      status:
        humanPresent: boolean
        fanOn: boolean
        lightOn: boolean
        motorState: "active" | "idle"
      config:
        autoOffEnabled: boolean
        autoOffDelayMs: number
        sensorSoundThreshold: number
        sensorLightThreshold: number
      command:
        runMotor: boolean
        direction: "forward" | "backward"
        executed: boolean
      lastSeen: timestamp
```

### Deploy to Firebase Hosting

```bash
npm run build
npx firebase deploy --only hosting
```

---

## 🧪 Testing Summary

We used a four-stage bottom-up testing framework:

### Stage 1 — Unit Testing
Each sensor tested in isolation before integration.
- mmWave calibrated for ideal detection distance (~1–3m for dorm rooms)
- Sound sensor frequency filter tuned to isolate fan hum from speech

### Stage 2 — System Testing
Weekly testing across multiple rooms to measure:
- Sensor accuracy under varying light conditions
- Motor reliability over repeated actuations

### Stage 3 — Integration Testing
Focus on cloud communication:
- Rapid toggle stress test (5 minutes continuous)
- Confirmed sub-second latency for control commands
- Server stability verified under high-frequency Firestore writes

### Stage 4 — Acceptance Testing
Real-world deployment in "Bilik Felo":
- Live test subject enters/exits room
- System correctly automated switch-off
- Physical mounting held firm on real wall switch

**Overall status accuracy: >90%** after sensor calibration.

---

## 🐛 Known Issues & Bugs Fixed

| Bug | Root Cause | Fix Applied |
|---|---|---|
| Motor "bangs" into housing | `delay()` too imprecise | Replaced with `MOTOR_RUN_TIME_MS` calibrated to 450–500ms |
| Fan status always "ON" | KY-037 picking up ambient noise | Added frequency-pattern filter in firmware |
| Device mounts poorly on multi-switch panels | Non-standard switch layouts | Redesigned bracket with adjustable mounting points |
| Presence false positives | mmWave too sensitive | Tuned detection sensitivity via UART configuration |

---

## 📚 Full References

- Alam, M. R., Reaz, M. B. I., & Ali, M. A. M. (2020). A review of smart homes — Past, present, and future. *Energies, 13*(15), 4035. https://doi.org/10.3390/en13154035
- Electronoobs. (2021). How to solder - 8 golden rules. https://www.youtube.com/watch?v=yKAJs2UZB6E
- ESP32IO. (n.d.). ESP32 tutorial. https://esp32io.com/
- ESP32IO. (2021). ESP32 - Photoresistor (GL55 series) tutorial. https://www.youtube.com/watch?v=5Aq_5n3zhaM
- Popular Science. (2015). Soldering basics. https://youtu.be/-THJq9LdazE
- Random Nerd Tutorials. (2019). ESP32 with DC motor and L298N motor driver. https://www.youtube.com/watch?v=E2sTbpFsvXI
- Zailani, N. F. B., & Othman, N. Z. B. (2024). *Getting started with Arduino and ESP32: A beginner's guide with Wokwi.* Politeknik Mersing. eISBN 978-967-2904-75-5