# 💡 Switch Off!!!

> An IoT-powered smart switch actuator that automatically turns off lights and fans when you leave the room — controlled remotely via a web dashboard.

**CT115/CT125 Digital Technology · Semester I/II 2025/2026 · TECH CC SDN BHD**

[![Demo](https://img.shields.io/badge/Live%20Demo-MVP-brightgreen?style=for-the-badge)](https://studio--switch-off-b68c4.us-central1.hosted.app/)
[![Platform](https://img.shields.io/badge/Platform-ESP32-blue?style=for-the-badge)]()
[![Firmware](https://img.shields.io/badge/Firmware-MicroPython-yellow?style=for-the-badge)]()
[![Backend](https://img.shields.io/badge/Backend-Firebase-orange?style=for-the-badge)]()
[![Web](https://img.shields.io/badge/Web-Next.js-black?style=for-the-badge)]()

---

## 🎯 Problem Statement

Students in dormitories routinely leave lights and fans running after leaving their rooms, leading to unnecessary energy waste, higher utility bills, and increased carbon emissions. Existing smart switch solutions require electrical rewiring — not feasible in a rented dorm environment.

## 💡 Our Solution

**Switch Off!!!** is a plug-and-play device that mounts **over** an existing wall switch without any electrical modification. It uses a motorised rack-and-pinion mechanism to physically flip the switch, controlled by an ESP32 microcontroller connected to Firebase via Wi-Fi.

Users can:
- **Monitor** room status (presence, light, fan) in real time via a web dashboard
- **Control** switches remotely from anywhere
- **Automate** switch-off when no human presence is detected for a set duration

---

## 🌐 Live Demo

👉 **[https://studio--switch-off-b68c4.us-central1.hosted.app/](https://studio--switch-off-b68c4.us-central1.hosted.app/)**

> MVP build — core monitoring and manual control features are live.

---

## 📁 Repository Structure

```
switch-off/
├── README.md                  ← You are here
├── firmware/
│   ├── README.md              ← Firmware setup & flashing guide
│   └── main.py                ← MicroPython source (ESP32)
├── hardware/
│   ├── README.md              ← Hardware assembly guide
│   ├── circuit_diagram.png    ← Wiring diagram (Cirkit Designer)
│   └── bom.md                 ← Bill of Materials
├── docs/
│   ├── README.md              ← Full project documentation
│   ├── report.pdf             ← Official project report
│   └── media/
│       ├── dashboard.png      ← Web dashboard screenshots
│       ├── prototype.jpg      ← Physical prototype photos
│       └── demo.mp4           ← Demo video
```

---

## 🔧 Hardware Overview

| Component | Role |
|---|---|
| ESP32 NodeMCU (ESP32S) | Main microcontroller — Wi-Fi, logic, motor control |
| GA12-N20 Geared Motor (3V 15RPM) | Physical switch actuation |
| L298N Mini Motor Driver | Motor direction & speed control |
| HLK-LD2410C mmWave Sensor | Human presence detection (motion + stationary) |
| GL55 LDR Sensor | Light level detection (switch ON/OFF status) |
| KY-037 Sound Sensor | Fan vibration/noise detection |
| Rack & Pinion + Metal Shaft | Converts motor rotation → linear switch movement |
| 5V 3A DC Adapter | System power supply |

> See [`hardware/README.md`](hardware/README.md) for full assembly instructions and [`hardware/bom.md`](hardware/bom.md) for sourcing details.

---

## 🖥️ Software Stack

| Layer | Technology |
|---|---|
| Firmware | MicroPython on ESP32 |
| Cloud / Database | Firebase Firestore |
| Web Dashboard | Next.js hosted on Firebase Hosting |
| 3D Enclosure Design | FreeCAD 1.0 |
| Circuit Design | Cirkit Designer |

---

## ⚡ How It Works

```
┌─────────────┐     Wi-Fi / Firestore       ┌──────────────────┐
│   ESP32     │ ◄─────────────────────────► │  Firebase Cloud  │
│             │                             └────────┬─────────┘
│  Sensors:   │                                      │ Real-time sync
│  • mmWave   │                             ┌────────▼─────────┐
│  • LDR      │                             │   Next.js Web    │
│  • Sound    │                             │   Dashboard      │
│             │                             │  (User Control)  │
│  Actuator:  │                             └──────────────────┘
│  • N20 Motor│
│  • L298N    │
└─────────────┘
       │
       ▼ Physical rack & pinion
  ┌─────────┐
  │  Wall   │
  │ Switch  │ ← flipped ON / OFF
  └─────────┘
```

**Auto-Off Logic:**
1. mmWave sensor continuously checks for human presence
2. If no presence detected + light/fan still ON → starts countdown timer
3. After delay threshold → motor activates to flip the switch OFF
4. Status synced to dashboard in real time

---

## 🚀 Getting Started

### Prerequisites
- ESP32 board (ESP32S / NodeMCU)
- MicroPython firmware flashed on the board
- Firebase project (Firestore enabled)
- Node.js 18+ (for web dashboard)

### 1. Flash the Firmware
See [`firmware/README.md`](firmware/README.md) for full flashing and configuration steps.

### 2. Configure Firebase
Update your Firestore credentials and device URL in `firmware/main.py`:
```python
WIFI_SSID = "your_wifi"
WIFI_PASS = "your_password"
DEVICE_URL = "your_firestore_device_url"
```

### 3. Run the Web Dashboard
```bash
cd web
npm install
npm run dev
```
Or deploy to Firebase Hosting — see [`docs/README.md`](docs/README.md).

---

## 📊 Test Results

| Test | Description | Result |
|---|---|---|
| TC-01 Unit | mmWave range detection (1m–5m) | ✅ Pass |
| TC-02 Unit | Sound sensor fan vs. speech isolation | ✅ Pass (after tuning) |
| TC-03 System | Environmental adaptability across rooms | ✅ Pass |
| TC-04 Integration | Data latency under rapid toggle | ✅ Pass (minor ms delay) |
| TC-05 Acceptance | Live subject real-world test ("Bilik Felo") | ✅ Pass |

Status accuracy after sensor calibration: **>90%**

---

## ⚠️ Known Limitations

- Requires constant plug-in power (no battery option yet)
- Multi-switch panels toggle all switches simultaneously (no individual control yet)
- Performance depends on Wi-Fi signal strength
- Regulator-style switches (positioned above the switch) are not currently supported

---

## 🔮 Future Work

- Support for a wider variety of switch types and configurations
- Individual switch control in multi-switch panels
- Battery / USB-C power option for portability
- User-friendly instruction manual with debugging guide
- Scheduling and energy usage analytics in the app

---

## 👥 Team — TECH CC SDN BHD

**TAIB HAZMI BIN TAIBRIZAL** • *Project Lead*

**MUHAMMAD ALTAMIS ZAFRAN BIN MOHD AFFENDY** • *Hardware Developer*

**MUHAMAD ZAID IZZUDDIN BIN NAZRI** • *Software Developer*

**NUR ERNA NADIRAH BINTI AMINUDDIN** • *System Designer*

---

## 📚 References

- Alam, M. R. et al. (2020). A review of smart homes — Past, present, and future. *Energies, 13*(15). https://doi.org/10.3390/en13154035
- Random Nerd Tutorials. ESP32 with DC motor and L298N motor driver. https://www.youtube.com/watch?v=E2sTbpFsvXI
- ESP32IO. ESP32 - Photoresistor (GL55 series) tutorial. https://esp32io.com/

---

## 📄 License

This project was developed as an academic submission for CT125 Digital Technology, Bahagian Matrikulasi, Kementerian Pendidikan Malaysia. All rights reserved.