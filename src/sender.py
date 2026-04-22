import machine
import time
import network
import socket

# --- CONFIGURATION ---
SSID = "Your_WiFi_Name"
PASSWORD = "Your_WiFi_Password"
MOTOR_IP = "192.168.1.100"  # Set this to the static IP of your Motor ESP
UDP_PORT = 1234

# Pin Definitions
trig = machine.Pin(12, machine.Pin.OUT)
echo = machine.Pin(13, machine.Pin.IN)
float_sw = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)
flow_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

# Flow Counter Setup
pulse_count = 0
def flow_callback(p):
    global pulse_count
    pulse_count += 1
flow_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=flow_callback)

# WiFi Connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print("Connecting to WiFi...")
    time.sleep(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def get_distance():
    trig.value(0)
    time.sleep_us(5)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    
    # Wait for echo pulse
    while echo.value() == 0: pass
    t1 = time.ticks_us()
    while echo.value() == 1: pass
    t2 = time.ticks_us()
    
    duration = time.ticks_diff(t2, t1)
    return (duration * 0.0343) / 2

# --- MAIN LOOP ---
while True:
    dist = get_distance()
    is_full = float_sw.value() == 0  # Assuming 0 is triggered/closed
    
    # Calculate Flow (Simplified)
    flow_val = pulse_count
    pulse_count = 0 
    
    # Determine Command
    # Send "OFF" if float switch is triggered OR water is too close (e.g., < 10cm)
    if is_full or dist < 10:
        cmd = b"MOTOR_OFF"
    else:
        cmd = b"MOTOR_ON"

    try:
        sock.sendto(cmd, (MOTOR_IP, UDP_PORT))
        print("Distance: {:.1f}cm | Sent: {}".format(dist, cmd.decode()))
    except Exception as e:
        print("Network Error:", e)

    time.sleep(1) # Send update every second