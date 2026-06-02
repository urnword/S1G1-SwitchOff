# 🔩 Hardware — Switch Off!!!

Assembly guide, wiring reference, and Bill of Materials for the Switch Off!!! smart switch actuator.

---

## 📁 Files

```
hardware/
├── README.md           ← This file (assembly guide)
├── circuit_diagram.png ← Full wiring diagram (Cirkit Designer)
├── enclosure.stl       ← Product 3d model ensclosure
└── bom.md              ← Bill of Materials with sourcing notes
```

---

## 🧩 Bill of Materials (Quick Reference)

| # | Component | Spec | Qty |
|---|---|---|---|
| 1 | ESP32 NodeMCU (ESP32S) | 38-pin, built-in Wi-Fi/BT | 1 |
| 2 | GA12-N20 Geared DC Motor | 3V, 15RPM | 1–4 |
| 3 | L298N Mini Motor Driver | Dual H-bridge | 1 |
| 4 | HLK-LD2410C mmWave Sensor | 24GHz FMCW radar | 1 |
| 5 | GL55 LDR Module | Light-dependent resistor | 1 |
| 6 | KY-037 Sound Sensor | Microphone + comparator | 1 |
| 7 | Rack & Pinion set | Plastic, compatible with N20 shaft | 1 |
| 8 | Metal shaft | 2mm diameter | 1 |
| 9 | 5V 3A DC Power Adapter | Regulated DC | 1 |
| 10 | DC Barrel Connector (female) | 5.5mm × 2.1mm | 1 |
| 11 | LED (red + green) | 5mm, with 220Ω resistors | 2 |
| 12 | Buzzer | 5V passive/active | 1 |
| 13 | Jumper wires | M-M and M-F assorted | — |
| 14 | Custom 3D-printed enclosure | Designed in FreeCAD 1.0 | 1 |

> Full sourcing details and approximate costs: see [`bom.md`](bom.md)

---

## 📐 Circuit Overview

The ESP32 sits at the centre of the circuit:

- **Inputs:** mmWave sensor (UART), LDR (ADC), Sound sensor (ADC)
- **Outputs:** L298N motor driver → N20 motor, LED indicators, Buzzer
- **Power:** 5V 3A adapter → DC connector → L298N onboard 5V regulator → ESP32 + sensors

See `circuit_diagram.png` in this folder for the full wiring diagram.

---

## 🔌 Wiring Guide

### Power Rails
```
5V Adapter (+) ──► DC Connector (+) ──► L298N 12V pin (works with 5V)
                                    └──► ESP32 VIN
GND ─────────────────────────────────── All component GNDs (common ground)
```

### Motor Driver (L298N) → ESP32
```
L298N IN1  ──► ESP32 GPIO 26
L298N IN2  ──► ESP32 GPIO 27
L298N OUT1 ──► N20 Motor terminal A
L298N OUT2 ──► N20 Motor terminal B
```

### Sensors → ESP32
```
HLK-LD2410C TX  ──► ESP32 GPIO 16 (RX2)
HLK-LD2410C RX  ──► ESP32 GPIO 17 (TX2)
HLK-LD2410C VCC ──► 3.3V
HLK-LD2410C GND ──► GND

GL55 LDR AO  ──► ESP32 GPIO 35 (ADC)
GL55 LDR VCC ──► 3.3V
GL55 LDR GND ──► GND

KY-037 AO  ──► ESP32 GPIO 34 (ADC)
KY-037 VCC ──► 3.3V
KY-037 GND ──► GND
```

### Indicators
```
LED (Red)   (+) ──► 220Ω ──► ESP32 GPIO 22
LED (Green) (+) ──► 220Ω ──► ESP32 GPIO 23
Buzzer (+)       ──────────► ESP32 GPIO 21
All (-) ─────────────────────────────── GND
```

---

## 🏗️ Physical Assembly

### Enclosure & Mount

The enclosure is 3D-printed using FreeCAD 1.0. The design:
- Mounts **around** the existing wall switch panel using a custom bracket
- Holds the N20 motor aligned with the switch toggle
- Has cable routing channels for clean wire management
- Attaches without screws into the wall (adhesive or clip-based)

> ⚠️ **Important:** This design works with standard toggle switches. Regulator-style (rotary) switches positioned above or beside the toggle are not currently supported.

### Rack & Pinion Mechanism

```
N20 Motor shaft
      │
      ▼
  [Pinion gear]  ←──rotates──►  [Rack gear (linear)]
                                        │
                                        ▼
                                  Metal shaft (2mm)
                                        │
                                        ▼
                                  Switch toggle
                                  (physical contact)
```

Motor rotates → pinion drives rack → rack pushes shaft → shaft flips switch.

**Critical:** Motor run time must be calibrated (450–500ms) to avoid the shaft hitting the housing. See firmware `MOTOR_RUN_TIME_MS`.

---

## ✅ Assembly Checklist

- [ ] Solder all header pins on ESP32 and L298N
- [ ] Wire all sensor connections with common GND
- [ ] Test motor direction (forward = switch ON, backward = switch OFF)
- [ ] Print and fit enclosure — verify rack alignment with switch toggle
- [ ] Attach LDR module facing toward the light indicator of the switch/bulb
- [ ] Mount KY-037 sound sensor facing toward the fan (ceiling or wall-mounted)
- [ ] Connect 5V adapter and verify ESP32 boots (LED blink / serial output)
- [ ] Flash firmware and confirm Wi-Fi + Firestore connection

---

## ⚠️ Safety Notes

- This device operates at **5V DC only** — it does not connect to mains wiring
- Do not expose the circuit to moisture
- Ensure the motor bracket is firmly fixed before sustained use — mechanical stress can loosen the mount over time
- The device draws up to ~3A under motor load; use a rated 5V 3A adapter
