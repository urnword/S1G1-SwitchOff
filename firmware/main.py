import machine
import time
import network
import urequests
import ujson
import utime
import ntptime
import _thread

# ================= PINS (ESP32-S) =================
RADAR_OUT_PIN = 4
KY037_A_PIN = 34
LDR_A_PIN   = 35
MOTOR_IN1 = 26
MOTOR_IN2 = 27
LED_GREEN = 18
LED_RED   = 19
BUZZER_PIN = 23

# ================= SETTINGS =================
MOTOR_RUN_TIME_MS = 9000
COMMAND_POLL_MS = 2000
WIFI_CHECK_MS = 5000
TIMEZONE_OFFSET = 8 * 3600

# ================= STATE =================
motor_active = False
human_present = False
last_status = {}
motor_start_ms = 0
last_seen_ms = 0
last_human_seen_ms = 0
auto_motor_ran_forward = False
auto_motor_ran_backward = False
firebase_connected = False
last_debug_print = 0

# ================= CONFIG =================
config = {
    "autoOffEnabled": False,
    "autoOffDelayMs": 600000,
    "sensorSoundThreshold": 2000,  # 0-4095 scale
    "sensorLightThreshold": 2000   # 0-4095 scale
}

command = {
    "runMotor": False,
    "direction": "forward",
    "executed": True
}

# ================= WIFI =================
SSID = "hotsiput"
PASSWORD = "12345678"
wifi = network.WLAN(network.STA_IF)

# ================= FIREBASE =================
PROJECT_ID = "switch-off-b68c4"
DEVICE_MAC = "11:22:33:44:55:66"
BASE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"
DEVICE_URL = f"{BASE_URL}/devices/{DEVICE_MAC}"

# ================= HARDWARE =================
motor1 = machine.Pin(MOTOR_IN1, machine.Pin.OUT)
motor2 = machine.Pin(MOTOR_IN2, machine.Pin.OUT)
led_green = machine.Pin(LED_GREEN, machine.Pin.OUT)
led_red   = machine.Pin(LED_RED, machine.Pin.OUT)
buzzer = machine.PWM(machine.Pin(BUZZER_PIN))
buzzer.duty_u16(0)
adc_sound = machine.ADC(machine.Pin(KY037_A_PIN))
adc_light = machine.ADC(machine.Pin(LDR_A_PIN))
radar = machine.Pin(RADAR_OUT_PIN, machine.Pin.IN)

# ================= WATCHDOG =================
wdt = machine.WDT(timeout=8000)

# ================= BUZZER =================
BUZZER_SOUNDS = {
    "wifi_ok":[(550,0.1),(660,0.1),(880,0.2)],
    "firebase_ok":[(880,0.3),(990,0.3)],
    "motor":[(440,0.1),(550,0.1),(660,0.1)],
    "error":[(220,0.4)]
}

def buzzer_play(name):
    if name not in BUZZER_SOUNDS:
        return
    for freq,dur in BUZZER_SOUNDS[name]:
        buzzer.freq(freq)
        buzzer.duty_u16(32768)
        time.sleep(dur)
        buzzer.duty_u16(0)
        time.sleep(0.05)

# ================= TIME =================
def sync_time():
    try:
        print("[NTP] Syncing time...")
        ntptime.settime()
        now = utime.time() + TIMEZONE_OFFSET
        tm = utime.localtime(now)
        print("[NTP] Synced: %04d-%02d-%02d %02d:%02d:%02d" %
              (tm[0],tm[1],tm[2],tm[3],tm[4],tm[5]))
        return True
    except Exception as e:
        print("[NTP] Failed:",e)
        buzzer_play("error")
        return False

def fs_now():
    t = utime.localtime(utime.time()+TIMEZONE_OFFSET)
    return {
        "timestampValue":"%04d-%02d-%02dT%02d:%02d:%02dZ" % (
            t[0],t[1],t[2],t[3],t[4],t[5]
        )
    }

# ================= HELPERS =================
def adc_avg(adc, n=5):
    s = 0
    for _ in range(n):
        s += adc.read_u16() >> 4  # convert 16-bit to 12-bit (0-4095)
        time.sleep_ms(2)
    return s // n

def read_radar():
    return radar.value()

def update_leds():
    if motor_active:
        led_red.value(1)
        led_green.value(0)
    else:
        led_red.value(0)
        led_green.value(1)

# ================= MOTOR =================
def start_motor(direction):
    global motor_active, motor_start_ms
    motor_active=True
    motor_start_ms=time.ticks_ms()
    if direction=="forward":
        motor1.value(1)
        motor2.value(0)
    else:
        motor1.value(0)
        motor2.value(1)
    update_leds()
    buzzer_play("motor")
    print("[MOTOR] start:",direction)

def stop_motor():
    global motor_active
    motor_active=False
    motor1.value(0)
    motor2.value(0)
    update_leds()
    print("[MOTOR] stopped")

def check_motor_timeout():
    if motor_active and time.ticks_diff(time.ticks_ms(), motor_start_ms)>=MOTOR_RUN_TIME_MS:
        stop_motor()

# ================= WIFI =================
def wifi_connect():
    if wifi.isconnected():
        return True
    print("[WIFI] Connecting...")
    wifi.active(True)
    wifi.connect(SSID,PASSWORD)
    start=time.ticks_ms()
    while not wifi.isconnected():
        if time.ticks_diff(time.ticks_ms(), start)>10000:
            print("[WIFI] Failed")
            buzzer_play("error")
            return False
        time.sleep(0.5)
    print("[WIFI] Connected:",wifi.ifconfig())
    sync_time()
    buzzer_play("wifi_ok")
    return True

# ================= FIRESTORE =================
def fetch_device():
    global config, command, firebase_connected
    try:
        r = urequests.get(DEVICE_URL)
        if r.status_code != 200:
            r.close()
            return False
        data = r.json()
        r.close()
        if "fields" not in data:
            return False
        fields = data["fields"]
        if not firebase_connected:
            print("[FIREBASE] Connected")
            buzzer_play("firebase_ok")
            firebase_connected = True
        if "config" in fields:
            c = fields["config"]["mapValue"]["fields"]
            config["autoOffEnabled"] = c["autoOffEnabled"]["booleanValue"]
            config["autoOffDelayMs"] = int(c["autoOffDelayMs"]["integerValue"])
            config["sensorSoundThreshold"] = int(c["sensorSoundThreshold"]["integerValue"])
            config["sensorLightThreshold"] = int(c["sensorLightThreshold"]["integerValue"])
        if "command" in fields:
            cmd = fields["command"]["mapValue"]["fields"]
            command["runMotor"] = cmd["runMotor"]["booleanValue"]
            command["direction"] = cmd["direction"]["stringValue"]
            command["executed"] = cmd["executed"]["booleanValue"]
        return True
    except Exception as e:
        print("[FIREBASE] Fetch error:",e)
        buzzer_play("error")
        return False

def patch_device(fields):
    try:
        masks = ["updateMask.fieldPaths="+k for k in fields]
        url = DEVICE_URL + "?" + "&".join(masks)
        r = urequests.patch(
            url,
            headers={"Content-Type":"application/json"},
            data=ujson.dumps({"fields":fields})
        )
        r.close()
    except Exception as e:
        print("[FIREBASE] Patch error:", e)

# ================= STATUS =================
def update_status(fan_on, light_on):
    global last_status
    current = {
        "humanPresent": human_present,
        "fanOn": fan_on,
        "lightOn": light_on,
        "motorState":"active" if motor_active else "idle"
    }
    if current != last_status:
        patch_device({
            "status": {"mapValue": {"fields": {
                "humanPresent":{"booleanValue":current["humanPresent"]},
                "fanOn":{"booleanValue":current["fanOn"]},
                "lightOn":{"booleanValue":current["lightOn"]},
                "motorState":{"stringValue":current["motorState"]},
                "updatedAt": fs_now()
            }}}
        })
        last_status = current

# ================= NETWORK THREAD =================
def network_thread():
    global last_seen_ms
    last_poll=0
    last_wifi_check=0
    while True:
        now=time.ticks_ms()
        if time.ticks_diff(now,last_wifi_check) > WIFI_CHECK_MS:
            if not wifi.isconnected():
                wifi_connect()
            last_wifi_check=now
        if wifi.isconnected() and time.ticks_diff(now,last_poll) > COMMAND_POLL_MS:
            fetch_device()
            last_poll=now
        if time.ticks_diff(now,last_seen_ms) > 60000:
            patch_device({"lastSeen": fs_now()})
            last_seen_ms=now
        time.sleep_ms(200)

# ================= STARTUP =================
wifi_connect()
last_human_seen_ms=time.ticks_ms()
_thread.start_new_thread(network_thread, ())
print("[SYSTEM] Ready")

# ================= MAIN LOOP =================
while True:
    wdt.feed()
    now=time.ticks_ms()
    human_present=read_radar()
    sound_val=adc_avg(adc_sound)
    light_val=adc_avg(adc_light)
    fan_on = sound_val > config["sensorSoundThreshold"]
    light_on = light_val > config["sensorLightThreshold"]

    if human_present:
        last_human_seen_ms=now
        auto_motor_ran_forward=False

    if config["autoOffEnabled"]:
        delay = time.ticks_diff(now, last_human_seen_ms)
        if (not human_present) and (fan_on or light_on) and delay >= config["autoOffDelayMs"]:
            if not motor_active and not auto_motor_ran_forward:
                start_motor("forward")
                auto_motor_ran_forward=True
                auto_motor_ran_backward=False

    if command["runMotor"] and not command["executed"] and not motor_active:
        start_motor(command["direction"])
        patch_device({
            "command":{"mapValue":{"fields":{
                "runMotor":{"booleanValue":False},
                "direction":{"stringValue":command["direction"]},
                "executed":{"booleanValue":True}
            }}}
        })

    check_motor_timeout()
    update_leds()
    update_status(fan_on, light_on)

    # ================= LIVE SENSOR DEBUG =================
    print("\rRadar:{} Sound:{} Light:{} Motor:{} WiFi:{} Firebase:{}"\
          .format(human_present, sound_val, light_val, motor_active, wifi.isconnected(), firebase_connected), end='')

    time.sleep_ms(200)
