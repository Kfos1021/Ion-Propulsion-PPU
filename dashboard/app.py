"""
@file app.py
@brief Ground-Station Real-Time Telemetry Dashboard for Spacecraft PPU

This script implements a real-time terminal user interface (TUI) to display
telemetry metrics for an Ion Propulsion Power Processing Unit (PPU). It tracks
channel voltages, active currents, output power, and overall system efficiency.
"""

import time
import os

class PPUDashboard:
    """
    @class PPUDashboard
    @brief Manages telemetry state variables, power calculations, and terminal UI rendering.
    """
    def __init__(self):
        """
        @brief Constructor: Initializes nominal PPU telemetry parameters.
        """
        # Active state flag from C++ state machine (e.g., OFF, STANDBY, THRUST)
        self.state = "THRUST"
        
        # Spacecraft main DC bus voltage (Volts)
        self.bus_voltage = 24.0
        
        # Beam Channel: High-voltage supply for ion acceleration (Volts, Amps)
        self.beam_voltage = 100.0
        self.beam_current = 0.20
        
        # Discharge Channel: Low-voltage supply for plasma ionization (Volts, Amps)
        self.discharge_voltage = 15.0
        self.discharge_current = 1.50
        
        # Board thermal monitoring sensor (°C)
        self.temperature = 42.5

    def calculate_metrics(self):
        """
        @brief Calculates active stage power and overall power conversion efficiency.
        @return tuple (p_out, p_in, efficiency) in Watts and Percentage.
        """
        # Calculate active output power per channel using P = V * I
        p_beam = self.beam_voltage * self.beam_current
        p_disch = self.discharge_voltage * self.discharge_current
        p_out = p_beam + p_disch

        # Estimate total input power assuming ~90% stage conversion efficiency
        # Prevents division by zero when output power is 0.0 W
        p_in = p_out / 0.90 if p_out > 0 else 0.1
        efficiency = (p_out / p_in) * 100.0 if p_in > 0 else 0.0

        return p_out, p_in, efficiency

    def render(self):
        """
        @brief Clears the console and renders the formatted telemetry display panel.
        """
        # Compute active power totals
        p_out, p_in, efficiency = self.calculate_metrics()
        
        # Clear the terminal canvas for smooth frame updates (Windows vs UNIX)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Render header and state panel
        print("==========================================================")
        print("       ION PROPULSION PPU GROUND-STATION TELEMETRY        ")
        print("==========================================================")
        print(f" OPERATIONAL STATE : [{self.state}]")
        print(f" SYSTEM TEMP      : {self.temperature:.1f} °C")
        print("----------------------------------------------------------")
        
        # Render individual power channel metrics
        print(" CHANNEL TELEMETRY:")
        print(f"   Spacecraft Bus : {self.bus_voltage:.2f} V")
        print(f"   Beam Supply    : {self.beam_voltage:.1f} V  |  {self.beam_current:.2f} A  |  {self.beam_voltage * self.beam_current:.2f} W")
        print(f"   Discharge      : {self.discharge_voltage:.1f} V  |  {self.discharge_current:.2f} A  |  {self.discharge_voltage * self.discharge_current:.2f} W")
        print("----------------------------------------------------------")
        
        # Render calculated efficiency metrics
        print(" POWER METRICS:")
        print(f"   Total Output Power : {p_out:.2f} W")
        print(f"   Total Input Power  : {p_in:.2f} W")
        print(f"   System Efficiency  : {efficiency:.1f} %")
        print("==========================================================")

if __name__ == "__main__":
    # Instantiate dashboard and render the initial UI panel
    dash = PPUDashboard()
    dash.render()