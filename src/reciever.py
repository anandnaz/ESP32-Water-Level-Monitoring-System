import machine
import network
import socket
import time

# --- CONFIGURATION ---
SSID = "Your_WiFi_Name"
PASSWORD = "Your_WiFi_Password"
UDP_PORT = 1234
RELAY_PIN = 5

relay = machine.Pin(RELAY_PIN, machine.Pin.OUT)
relay.value(1) # Start with Relay OFF (Assuming Active Low)

# WiFi Connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(1)

print("Motor ESP Connected. IP:", wlan.ifconfig()[0])

# Setup UDP Server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', UDP_PORT))
sock.settimeout(0.1) # Don't block forever

last_seen = time.time()

# --- MAIN LOOP ---
while True:
    try:
        data, addr = sock.recvfrom(1024)
        msg = data.decode().strip()
        last_seen = time.time() # Update watchdog timer

        if msg == "MOTOR_OFF":
            relay.value(1) # Turn OFF
            print("Status: STOPPED")
        elif msg == "MOTOR_ON":
            relay.value(0) # Turn ON
            print("Status: RUNNING")
            
    except OSError:
        # This happens when no data is received (timeout)
        pass

    # SAFETY FAIL-SAFE
    # If no signal for 10 seconds, shut down motor for safety
    if time.time() - last_seen > 10:
        relay.value(1)
        print("CRITICAL: Signal Lost! Motor Safety Cut-off.")
    
    time.sleep(0.1)