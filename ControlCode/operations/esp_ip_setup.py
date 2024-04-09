import serial
import socket

SEND_SUCCESS = 0

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def send_data(data):
    global SEND_SUCCESS
    try:
        ser = serial.Serial('/dev/ttyUSB0', 115200)  # TODO Replace '/dev/ttyUSB0' with Arduino's serial port
        if ser.isOpen():
            print("Serial connection established.")
            ser.write(data.encode())  # Convert string to bytes and send it
            print("Data sent:", data)
            ser.close()
            print("Serial connection closed.")
            SEND_SUCCESS = 1
        else:
            print("Serial connection failed.")
    except Exception as e:
        print("Error:", str(e))

data = get_ip_address()

for i in range(0,10):
    if not SEND_SUCCESS:
        send_data(data)  # Convert string to bytes and send it
    else:
        break
    