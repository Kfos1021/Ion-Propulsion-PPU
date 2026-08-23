class ThrusterModel:
    def __init__(self):
        # Nominal system voltages (Volts)
        self.v_beam = 100.0
        self.v_discharge = 15.0
        self.v_neutralizer = 12.0
        
        # Operational limits
        self.state = "OFF"  # Options: OFF, STANDBY, BEAM_ON
        self.throttle = 0.0  # 0.0 to 1.0 (0% to 100%)

    def set_state(self, new_state: str):
        valid_states = ["OFF", "STANDBY", "BEAM_ON"]
        if new_state in valid_states:
            self.state = new_state
        else:
            raise ValueError(f"Invalid state: {new_state}")

    def set_throttle(self, level: float):
        self.throttle = max(0.0, min(1.0, level))

    def get_currents(self):
        """Returns channel currents (Amps) based on current state & throttle."""
        if self.state == "OFF":
            return {"i_beam": 0.0, "i_discharge": 0.0, "i_neutralizer": 0.0}
        
        elif self.state == "STANDBY":
            # Idle housekeeping loads
            return {"i_beam": 0.0, "i_discharge": 0.2, "i_neutralizer": 0.1}
            
        elif self.state == "BEAM_ON":
            # Dynamic loads scaled by throttle setting
            i_beam = 0.05 + (0.15 * self.throttle)         # 50mA to 200mA
            i_discharge = 0.5 + (1.0 * self.throttle)      # 0.5A to 1.5A
            i_neutralizer = 0.1 + (0.2 * self.throttle)    # 0.1A to 0.3A
            return {"i_beam": i_beam, "i_discharge": i_discharge, "i_neutralizer": i_neutralizer}

    def get_power(self):
        """Calculates total load power consumption in Watts."""
        currents = self.get_currents()
        p_beam = self.v_beam * currents["i_beam"]
        p_discharge = self.v_discharge * currents["i_discharge"]
        p_neutralizer = self.v_neutralizer * currents["i_neutralizer"]
        return p_beam + p_discharge + p_neutralizer


if __name__ == "__main__":
    # Sanity check
    thruster = ThrusterModel()
    print("Initial State (OFF):", thruster.get_currents())
    
    thruster.set_state("BEAM_ON")
    thruster.set_throttle(0.5)  # 50% throttle
    print("50% Throttle Currents:", thruster.get_currents())
    print(f"Total Power: {thruster.get_power():.2f} W")