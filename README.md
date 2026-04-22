# Smart Water Tank Overflow & Usage Intelligence System

An IoT-based system to prevent water overflow, monitor usage, detect faults, and automatically control water pumps using ESP32.

<img width="350" height="200" alt="Gemini_Generated_Image_jctsfbjctsfbjcts" src="https://github.com/user-attachments/assets/c315dd5d-4c75-4e7d-8535-32116fc3f455" />

---

## Problem

- Water overflow in tanks → wastage
- No visibility of daily usage
- Pumps run • dry run damage blindly
- Existing solutions = basic alarms only

---

## Solution

A dual-node IoT system:

- 🛢️ Tank Node (Solar Powered)
    - Monitors water level, flow, and overflow
- ⚡ Control Node
    - Controls pump via contactor
    - Applies intelligent logic

---

## Features

- ✅ Automatic motor ON/OFF
- ✅ Overflow prevention
- ✅ Dry run detection (with current sensor - optional)
- ✅ Water usage tracking
- ✅ Leakage detection
- ✅ Solar-powered tank node
- ✅ WiFi communication (ESP32 ↔ ESP32)

---

## System Architecture

  *Tank Node ESP32*
    ├─ Ultrasonic Sensor (Level)
    ├─ Flow Sensor (Usage)
    ├─ Float Switch (Fail-safe)
    └─ Solar + Battery Power
    
  *Control Node ESP32*
    ├─ Relay → Contactor → Motor
    ├─ Current Sensor (optional)
    └─ AC Powered

---

## Hardware Components

### 🟢 Tank Node

- ESP32 DevKit V1
- JSN-SR04T Ultrasonic Sensor
- YF-S201 Flow Sensor
- Float Switch
- 10W Solar Panel
- 2× 18650 Batteries (series)
- 2S BMS
- CC/CV Charging Module
- MP1584 Buck Converter
- 1000µF Capacitor
- 0.1µF Capacitor
- Switch
- IP65 Enclosure

### 🔴 Control Node

- ESP32 DevKit V1
- Relay Module (5V, opto-isolated)
- Contactor (e.g., Schneider / L&T)      **Already present in the starter box**
- MCB (10A–16A)      **Already present in the starter box**
- ACS712 Current Sensor (optional)
- 5V SMPS

---

##🔌 Wiring Overview

### Tank Node

Solar → Charger → Battery → BMS → Buck (5V) → ESP32

Sensors:
Ultrasonic → GPIO 5,18
Flow → GPIO 19 (interrupt)
Float → GPIO 21

<img width="350" height="200" alt="tank side" src="https://github.com/user-attachments/assets/46e603fe-5e39-4b10-ba2a-6b06c7c6a974" />

### Control Node

SMPS → ESP32 → Relay → Contactor Coil (A1/A2)

Current Sensor → ESP32 ADC

<img width="350" height="200" alt="main side" src="https://github.com/user-attachments/assets/21673dbc-2bb0-4759-9bde-5e3616a02c18" />

---

## Communication

- Protocol: HTTP (initial)
- Future upgrade: MQTT
- Both ESP32s connect via the same WiFi network

---

## Logic

### Control Node:

- If level < 30% → Motor ON
- If level > 90% → Motor OFF
- Float triggered → Emergency OFF

### Tank Node:
- Sends:
    - Water level
    - Flow rate
    - Float status

---

## Power Design (Tank Node)

- Voltage: 5V regulated
- Current: 300–500 mA
- Solar Panel: 10W recommended
- Battery: ~6000 mAh (2×18650)

---

## Safety Considerations

- ❗ Use a contactor for the motor (never direct relay)
- ❗ Proper earthing required
- ❗ Use BMS for battery protection
- ❗ Separate high voltage and low voltage wiring
- ❗ Waterproof enclosure (IP65 recommended)

---

## Future Improvements

- 📱 Mobile app dashboard
- ☁️ Cloud data logging
- 🤖 Predictive water usage
- 🔔 Alert system (SMS/Push)
- ⚡ Energy monitoring

---

## Key Learnings

- Power design is more critical than code
- Sensor redundancy improves reliability
- Proper electrical isolation is mandatory

---

## Contribution

Feel free to:

- Improve logic
- Add UI/dashboard
- Optimise power usage

---

## Author

Anurag Anand




