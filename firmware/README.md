# ⚙️ Firmware — Switch Off!!!

MicroPython firmware for the ESP32 NodeMCU that drives the Switch Off!!! smart switch actuator.

---

## 📋 Prerequisites

- ESP32 board (ESP32S / NodeMCU recommended)
- [MicroPython firmware](https://micropython.org/download/esp32/) flashed on the board
- [Thonny IDE](https://thonny.org/) **or** `mpremote` / `ampy` for uploading files
- Firebase Firestore project with a device document set up
- Wi-Fi network (2.4GHz)

---

## 📁 Files

```
firmware/
├── README.md       ← This file
└── main.py         ← Main firmware (runs automatically on boot)
```

---

## 🔌 Pin Mapping

| ESP32 GPIO | Connected To |
|---|---|
| GPIO 26 | L298N IN1 (Motor forward) |
| GPIO 27 | L298N IN2 (Motor backward) |
| GPIO 34 | KY-037 Sound Sensor (ADC) |
| GPIO 35 | GL55 LDR Sensor (ADC) |
| GPIO 16 (RX2) | HLK-LD2410C mmWave TX |
| GPIO 17 (TX2) | HLK-LD2410C mmWave RX |

> Adjust GPIO numbers in `main.py` if your wiring differs.

---

## ⚡ Setup & Flashing

### Step 1 — Flash MicroPython to the ESP32

If MicroPython is not already on your board:

```bash
# Install esptool
pip install esptool

# Erase flash
esptool.py --port COM3 erase_flash

# Flash MicroPython (replace with your .bin path and port)
esptool.py --port COM3 write_flash -z 0x1000 esp32-micropython.bin
```

> On Linux/macOS, replace `COM3` with `/dev/ttyUSB0` or similar.

### Step 2 — Configure credentials

Edit `main.py` and update the following constants at the top of the file:

```python
WIFI_SSID     = "your_wifi_name"
WIFI_PASS     = "your_wifi_password"
FIRESTORE_URL = "https://firestore.googleapis.com/v1/projects/YOUR_PROJECT/databases/(default)/documents/devices/YOUR_DEVICE_ID"
```

### Step 3 — Upload to ESP32

**Using Thonny:**
1. Open Thonny → Select interpreter: MicroPython (ESP32)
2. Open `main.py`
3. File → Save As → MicroPython device → save as `main.py`
4. Press the reset button on the ESP32

**Using mpremote:**
```bash
pip install mpremote
mpremote connect COM3 cp firmware/main.py :main.py
mpremote connect COM3 reset
```

---

## 🧠 Firmware Logic Overview

### Key Functions

| Function | Description |
|---|---|
| `start_motor(direction)` | Activates motor in `"forward"` or `"backward"` direction |
| `stop_motor()` | Stops the motor immediately |
| `check_motor_timeout()` | Auto-stops motor after calibrated run time (~450–500ms) |
| `read_radar()` | Reads human presence from HLK-LD2410C via UART |
| `fetch_device()` | Pulls config & commands from Firestore |
| `patch_device(fields)` | Pushes status updates to Firestore |
| `network_thread()` | Background thread managing Wi-Fi + cloud sync |
| `update_status(fan_on, light_on)` | Sends status to cloud only on change (efficient) |

### Auto-Off Logic

```python
if config["autoOffEnabled"]:
    if (not human_present) and (fan_on or light_on):
        if delay >= config["autoOffDelayMs"]:
            start_motor("forward")
```

The motor only runs for the calibrated `MOTOR_RUN_TIME_MS` duration, preventing it from hitting the housing (the "banging bug" fix).

---

## 🔧 Configuration (via Web Dashboard)

The following settings can be changed at runtime through the web dashboard — no reflashing needed:

| Setting | Description |
|---|---|
| `autoOffEnabled` | Enable/disable the auto-off feature |
| `autoOffDelayMs` | How long (ms) to wait after presence lost before switching off |
| `sensorSoundThreshold` | ADC threshold for detecting fan ON state |
| `sensorLightThreshold` | ADC threshold for detecting light ON state |

---

## 🐛 Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Motor bangs into housing | `MOTOR_RUN_TIME_MS` too high | Reduce to ~450ms |
| Presence always detected | mmWave sensitivity too high | Adjust sensor sensitivity via UART config |
| Fan status incorrect | Sound threshold wrong | Increase `sensorSoundThreshold` in dashboard |
| Won't connect to Wi-Fi | Wrong credentials or 5GHz network | Ensure 2.4GHz SSID is used |
| No Firestore updates | Wrong `FIRESTORE_URL` | Double-check project ID and document path |