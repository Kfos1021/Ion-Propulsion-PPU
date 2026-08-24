"""
@file test_advanced_faults.py
@brief Automated Verification Suite for Advanced PPU Fault Scenarios
"""

import sys
import os
import unittest

# Ensure simulation directory is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../simulation')))
from thruster_model import ThrusterModel

class TestAdvancedFaults(unittest.TestCase):
    """
    @class TestAdvancedFaults
    @brief Test fixture validating critical safety limits and fault handling.
    """

    def setUp(self):
        """
        @brief Instantiates a clean ThrusterModel instance before each test.
        """
        self.plant = ThrusterModel()

    def test_beam_arc_overcurrent_fault(self):
        """
        @brief Validates that a Beam Arc event triggers an immediate overcurrent condition.
        """
        self.plant.set_state("BEAM_ON")
        self.plant.set_throttle(1.0)
        
        # Inject plasma arc short-circuit
        self.plant.inject_fault("BEAM_ARC")
        currents = self.plant.get_currents()
        
        # Verify beam current exceeds safety threshold
        self.assertGreater(currents["i_beam"], 2.0, "Beam Arc failed to trigger overcurrent condition.")

    def test_open_load_disconnect(self):
        """
        @brief Validates open-circuit load disconnection handling.
        """
        self.plant.set_state("BEAM_ON")
        self.plant.set_throttle(1.0)
        
        # Inject open load fault
        self.plant.inject_fault("OPEN_LOAD")
        currents = self.plant.get_currents()
        
        # Verify discharge current drops to zero
        self.assertEqual(currents["i_discharge"], 0.0, "Open load fault failed to clear discharge current.")

    def test_bus_undervoltage_isolation(self):
        """
        @brief Validates system behavior during bus undervoltage conditions (<18V).
        """
        self.plant.inject_fault("BUS_UNDERVOLTAGE")
        voltage = self.plant.get_bus_voltage()
        
        # Verify bus voltage sags below threshold
        self.assertLessEqual(voltage, 18.0, "Bus voltage failed to register undervoltage condition.")

    def test_startup_timeout_reset(self):
        """
        @brief Validates plant state isolation on uninitialized state transitions.
        """
        self.plant.set_state("OFF")
        currents = self.plant.get_currents()
        
        # Verify all currents are strictly zero in OFF state
        self.assertEqual(currents["i_beam"], 0.0)
        self.assertEqual(currents["i_discharge"], 0.0)
        self.assertEqual(currents["i_neutralizer"], 0.0)

if __name__ == "__main__":
    print("--- Running Day 19 Advanced Fault Injection Suite ---")
    unittest.main(verbosity=2)