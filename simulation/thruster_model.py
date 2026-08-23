class ThrusterModel:
    def __init__(self):
        # Nominal system voltages (Volts)
        self.v_bus = 24.0
        self.v_beam = 100.0
        self.v_discharge = 15.0
        self.v_neutralizer = 12.0
        
        # Operational limits
        self.state = "OFF"  # Options: OFF, STANDBY, BEAM_ON
        self.throttle = 0.0  # 0.0 to 1.0
        
        # Fault injection flags
        self.active_fault = None  # Options: None, "BEAM_ARC", "OPEN_LOAD", "BUS_UNDERVOLTAGE"

    def set_state(self, new_state: str):
        valid_states = ["OFF", "STANDBY", "BEAM_ON"]
        if new_state in valid_states:
            self.state = new_state
        else:
            raise ValueError(f"Invalid state: {new_state}")

    def set_throttle(self, level: float):
        self.throttle = max(0.0, min(1.0, level))

    def inject_fault(self, fault_name: str):
        """Simulates an active fault condition."""
        valid_faults = [None, "BEAM_ARC", "OPEN_LOAD", "BUS_UNDERVOLTAGE"]
        if fault_name in valid_faults:
            self.active_fault = fault_name
        else:
            raise ValueError(f"Invalid fault: {fault_name}")

    def get_currents(self):
        """Returns channel currents (Amps) including active fault dynamics."""
        if self.state == "OFF":
            return {"i_beam": 0.0, "i_discharge": 0.0, "i_neutralizer": 0.0}

        # Base currents
        if self.state == "STANDBY":
            i_beam, i_discharge, i_neutralizer = 0.0, 0.2, 0.1
        else:  # BEAM_ON
            i_beam = 0.05 + (0.15 * self.throttle)
            i_discharge = 0.5 + (1.0 * self.throttle)
            i_neutralizer = 0.1 + (0.2 * self.throttle)

        # Apply fault behaviors
        if self.active_fault == "BEAM_ARC":
            i_beam = 2.5  # High current spike simulating plasma short circuit
        elif self.active_fault == "OPEN_LOAD":
            i_discharge = 0.0  # Disconnected line / open load
        elif self.active_fault == "BUS_UNDERVOLTAGE":
            # Current scales up to maintain power on lower bus voltage
            i_beam *= 1.3
            i_discharge *= 1.3

        return {"i_beam": i_beam, "i_discharge": i_discharge, "i_neutralizer": i_neutralizer}

    def get_bus_voltage(self):
        """Returns supply bus voltage in Volts."""
        if self.active_fault == "BUS_UNDERVOLTAGE":
            return 18.0  # Sagged bus voltage (nominal 24V)
        return self.v_bus


if __name__ == "__main__":
    thruster = ThrusterModel()
    thruster.set_state("BEAM_ON")
    thruster.set_throttle(1.0)
    
    print("--- Nominal Full Power ---")
    print("Currents:", thruster.get_currents())
    
    print("\n--- Injecting BEAM_ARC Fault ---")
    thruster.inject_fault("BEAM_ARC")
    print("Currents:", thruster.get_currents())
    
    print("\n--- Injecting BUS_UNDERVOLTAGE Fault ---")
    thruster.inject_fault("BUS_UNDERVOLTAGE")
    print("Bus Voltage:", thruster.get_bus_voltage(), "V")
    print("Currents:", thruster.get_currents())