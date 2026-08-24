import socket
import time

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))
    
    # Receive command from C++
    data = client.recv(1024).decode('utf-8')
    print(f"[PYTHON SIM] Received Command from C++: {data.strip()}")
    
    # Send simulated telemetry back
    telemetry = "V_BUS:24.0,I_BEAM:0.25,I_DISCH:1.20,TEMP:42.5"
    client.send(telemetry.encode('utf-8'))
    print(f"[PYTHON SIM] Sent Telemetry to C++: {telemetry}")
    
    client.close()

if __name__ == "__main__":
    run_client()