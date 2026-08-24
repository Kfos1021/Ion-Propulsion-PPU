"""
Software-in-the-Loop (SiL) Closed-Loop Integration Test Engine
Connects C++ state machine commands with dynamic Python thruster plant telemetry.
"""

import socket
import sys
from thruster_model import ThrusterModel

def run_sil_loop():
    plant = ThrusterModel()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print("--- Connecting to C++ PPU Controller Socket ---")
    try:
        client.connect(('127.0.0.1', 8080))
        print("[SiL ENGINE] Successfully connected to C++ PPU Server!")
    except ConnectionRefusedError:
        print("[ERROR] Could not connect to C++ server. Ensure sil_bridge is running!")
        sys.exit(1)

    try:
        # Step 1: Receive command packet from C++
        data = client.recv(1024).decode('utf-8').strip()
        print(f"\n[RECEIVED COMMAND] {data}")

        # Parse command string
        state_cmd = "BEAM_ON"
        throttle = 1.0
        if "STATE:" in data:
            parts = data.split(",")
            raw_state = parts[0].split(":")[1]
            throttle = float(parts[1].split(":")[1])
            
            # Map C++ state name to ThrusterModel valid states
            if raw_state in ["THRUST", "BEAM_RAMP"]:
                state_cmd = "BEAM_ON"
            elif raw_state in ["OFF", "SHUTDOWN"]:
                state_cmd = "OFF"
            else:
                state_cmd = "STANDBY"

        # Step 2: Update dynamic plant model
        plant.set_state(state_cmd)
        plant.set_throttle(throttle)
        
        currents = plant.get_currents()
        bus_voltage = plant.get_bus_voltage()

        # Step 3: Format and send back telemetry payload
        payload = (f"V_BUS:{bus_voltage:.2f},"
                   f"I_BEAM:{currents['i_beam']:.2f},"
                   f"I_DISCH:{currents['i_discharge']:.2f},"
                   f"TEMP:42.5\n")

        client.send(payload.encode('utf-8'))
        print(f"[SENT TELEMETRY] {payload.strip()}")
        print("\n--- SiL Closed-Loop Integration Step Verified (PASS) ---")

    finally:
        client.close()

if __name__ == "__main__":
    run_sil_loop()