# 🛒 Bill of Materials — Switch Off!!!

All components used in the Switch Off!!! prototype.

> Prices are approximate and based on local Malaysian suppliers (Shopee MY / Lazada MY / component shops). As of April 2026.

---

## Hardware Components

| # | Component | Spec / Model | Est. Price (MYR) | Source |
|---|---|---|---|---|
| 1 | ESP32 NodeMCU | ESP32S, 38-pin | RM 15–20 | Shopee MY |
| 2 | GA12-N20 Geared DC Motor | 3V, 15RPM (×2 for dual switch) | RM 8–12 each | Shopee MY |
| 3 | L298N Mini Motor Driver | Mini version (not full-size) | RM 5–8 | Shopee MY / Lazada |
| 4 | HLK-LD2410C mmWave Sensor | 24GHz FMCW radar presence | RM 15–25 | Shopee MY |
| 5 | GL55 LDR Sensor Module | GL5516 or GL55 series | RM 2–4 | Shopee MY |
| 6 | KY-037 Sound Sensor | With adjustable comparator | RM 3–5 | Shopee MY |
| 7 | Rack & Pinion Gear Set | Plastic, fits 2mm N20 shaft | RM 5–10 | Shopee MY |
| 8 | Metal Shaft | 2mm diameter, ~50mm length | RM 1–3 | Hardware store |
| 9 | 5V 3A DC Power Adapter | UK plug (Malaysia standard) | RM 10–15 | Shopee MY |
| 10 | DC Barrel Connector (female) | 5.5mm × 2.1mm PCB or wire | RM 1–2 | Shopee MY |
| 11 | LED (red & green) | 5mm with 220Ω resistors | RM 1–2 | Component shop |
| 12 | Buzzer | 5V passive | RM 1–2 | Component shop |
| 13 | Jumper Wires | M-M, M-F, 20cm assorted | RM 3–5 | Shopee MY |
| 14 | 3D Print Filament (PLA) | For enclosure (~50–80g) | RM 5–10 | Printing service |

---

## Estimated Total Cost

| Tier | Cost (MYR) |
|---|---|
| Minimum (single switch unit) | ~RM 80–100 |
| Full prototype (as built) | ~RM 120–150 |

> Significantly cheaper than commercial smart switch solutions (Xiaomi, TP-Link Tapo, etc. which cost RM 60–150+ **and** require wiring modification). Switch Off!!! is non-invasive.

---

## Tools Required

| Tool | Purpose |
|---|---|
| Soldering iron + solder | Soldering headers and connections |
| Multimeter | Voltage & continuity checks |
| USB-to-microUSB cable | Flashing ESP32 |
| 3D printer or printing service | Printing the enclosure |
| Hot glue gun | Securing motor and sensors in enclosure |
| Small screwdrivers | Assembly |

---

## Software (Free / Open Source)

| Software | Purpose | License |
|---|---|---|
| MicroPython | ESP32 firmware | MIT |
| Thonny IDE | Firmware upload & debug | MIT |
| FreeCAD 1.0 | Enclosure 3D design | LGPL |
| Cirkit Designer | Circuit diagram | Free tier |
| Next.js | Web dashboard | MIT |
| Firebase | Cloud database & hosting | Free tier (Spark plan) |