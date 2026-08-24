"""
@file app.py
@brief Ground-Station Real-Time Telemetry Dashboard with CSV Logging
"""

import time
import os
import csv

class PPUDashboard:
    def __init__(self, log_file="dashboard/telemetry_log.csv"):
        self.state = "THRUST"
        self.bus_voltage = 24.0
        self.beam_voltage = 100.0
        self.beam_current = 0.20
        self.discharge_voltage = 15.0
        self.discharge_current = 1.50
        self.temperature = 42.5
        self.log_file = log_file

        # Initialize CSV header if file doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "state", "bus_voltage", 
                    "beam_voltage", "beam_current", 
                    "discharge_voltage", "discharge_current", 
                    "temperature", "p_out", "p_in", "efficiency"
                ])

    def calculate_metrics(self):
        p_beam = self.beam_voltage * self.beam_current
        p_disch = self.discharge_voltage * self.discharge_current
        p_out = p_beam + p_disch
        p_in = p_out / 0.90 if p_out > 0 else 0.1
        efficiency = (p_out / p_in) * 100.0 if p_in > 0 else 0.0
        return p_out, p_in, efficiency

    def log_telemetry(self):
        p_out, p_in, efficiency = self.calculate_metrics()
        with open(self.log_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"), self.state, 
                f"{self.bus_voltage:.2f}", f"{self.beam_voltage:.1f}", 
                f"{self.beam_current:.2f}", f"{self.discharge_voltage:.1f}", 
                f"{self.discharge_current:.2f}", f"{self.temperature:.1f}", 
                f"{p_out:.2f}", f"{p_in:.2f}", f"{efficiency:.1f}"
            ])

    def render(self):
        p_out, p_in, efficiency = self.calculate_metrics()
        self.log_telemetry()
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==========================================================")
        print("       ION PROPULSION PPU GROUND-STATION TELEMETRY        ")
        print("==========================================================")
        print(f" OPERATIONAL STATE : [{self.state}]")
        print(f" SYSTEM TEMP      : {self.temperature:.1f} °C")
        print("----------------------------------------------------------")
        print(" CHANNEL TELEMETRY:")
        print(f"   Spacecraft Bus : {self.bus_voltage:.2f} V")
        print(f"   Beam Supply    : {self.beam_voltage:.1f} V  |  {self.beam_current:.2f} A  |  {self.beam_voltage * self.beam_current:.2f} W")
        print(f"   Discharge      : {self.discharge_voltage:.1f} V  |  {self.discharge_current:.2f} A  |  {self.discharge_voltage * self.discharge_current:.2f} W")
        print("----------------------------------------------------------")
        print(" POWER METRICS:")
        print(f"   Total Output Power : {p_out:.2f} W")
        print(f"   Total Input Power  : {p_in:.2f} W")
        print(f"   System Efficiency  : {efficiency:.1f} %")
        print(f" LOG STATUS        : Saved to {self.log_file}")
        print("==========================================================")

if __name__ == "__main__":
    dash = PPUDashboard()
    dash.render()