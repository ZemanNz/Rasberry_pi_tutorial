import serial, time

ser = serial.Serial('/dev/serial0', 115200, timeout=1)
time.sleep(2)  # nech interface nastartovat

# odeslat zprávu
ser.write(b'Ahoj ESP32!\n')
print("Odesláno: Ahoj ESP32!")

# přijímat zprávy
while True:
    ser.write(b'ahoj\n')
    if ser.in_waiting:
        line = ser.readline().decode().strip()
        print("Přijato:", line)
    time.sleep(0.5)
