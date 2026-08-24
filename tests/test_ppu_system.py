"""
@file test_ppu_system.py
@brief Automated System Verification Suite for PPU Controller & Plant Model

This module runs automated unit and integration tests against the PPU thruster 
plant model using Python's unittest framework. It verifies operational state 
transitions, channel current limits, and dynamic fault detection boundaries.
"""

import sys
import os
import unittest

# Resolve module import path to ensure the simulation directory is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../simulation')))
from thruster_model import ThrusterModel

class TestPPUSystem(unittest.TestCase):
    """
    @class TestPPUSystem
    @brief Test fixture containing automated validation cases for PPU hardware behaviors.
    """
    
    def setUp(self):
        """
        @brief Test Setup Hook: Instantiates a clean ThrusterModel plant instance 
        before every test case to ensure zero test cross-contamination.
        """
        self.plant = ThrusterModel()

    def test_nominal_state_transitions(self):
        """
        @brief Validates state machine transition handling and throttle mapping.
        Verifies that state variables update cleanly without raising errors.
        """
        # Step 1: Transition to low-power STANDBY mode
        self.plant.set_state("STANDBY")
        self.assertEqual(self.plant.state, "STANDBY", "Plant failed to transition to STANDBY state.")
        
        # Step 2: Transition to full BEAM_ON mode and adjust throttle to 80%
        self.plant.set_state("BEAM_ON")
        self.plant.set_throttle(0.8)
        self.assertEqual(self.plant.state, "BEAM_ON", "Plant failed to transition to BEAM_ON state.")
        self.assertAlmostEqual(self.plant.throttle, 0.8, places=2, msg="Throttle level misaligned from setpoint.")

    def test_nominal_current_draws(self):
        """
        @brief Validates output channel currents during nominal 100% steady-state thrusting.
        Ensures beam and discharge currents remain within nominal operating windows.
        """
        # Drive plant model to 100% full power operation
        self.plant.set_state("BEAM_ON")
        self.plant.set_throttle(1.0)
        currents = self.plant.get_currents()
        
        # Assert Beam current equals nominal setpoint (~0.20 A) at full throttle
        self.assertAlmostEqual(currents["i_beam"], 0.20, places=2, 
                               msg="Beam current out of nominal limits at 100% throttle.")
        
        # Assert Discharge current is active and strictly greater than 1.0 A
        self.assertGreater(currents["i_discharge"], 1.0, 
                           msg="Discharge current below minimum ionization threshold.")

    def test_beam_arc_fault_detection(self):
        """
        @brief Tests system response to an injected high-voltage Beam Arc event.
        Verifies that a simulated short circuit produces an overcurrent spike > 2.0 A.
        """
        # Establish steady-state operation
        self.plant.set_state("BEAM_ON")
        self.plant.set_throttle(1.0)
        
        # Inject an active plasma short-circuit fault
        self.plant.inject_fault("BEAM_ARC")
        currents = self.plant.get_currents()
        
        # Verify that beam current spikes past the critical 2.0 A safety trip limit
        self.assertGreater(currents["i_beam"], 2.0, 
                           msg="Beam Arc fault failed to trigger overcurrent condition.")

    def test_bus_undervoltage_behavior(self):
        """
        @brief Tests bus voltage monitoring under abnormal supply drop conditions.
        Verifies that an injected undervoltage fault drops the sensed rail voltage below 20V.
        """
        # Inject bus supply sag fault
        self.plant.inject_fault("BUS_UNDERVOLTAGE")
        voltage = self.plant.get_bus_voltage()
        
        # Confirm sensed bus voltage sags below the minimum 20.0 V threshold
        self.assertLess(voltage, 20.0, 
                        msg="Bus undervoltage fault failed to register expected voltage sag.")

if __name__ == "__main__":
    print("--- Running Automated PPU System Verification Suite ---")
    # Execute all test cases with verbose terminal logging
    unittest.main(verbosity=2)