/**
 * @file main.cpp
 * @brief Bare-Metal C++ Ion Propulsion Power Processing Unit (PPU) Controller
 * 
 * Implements the core 8-state sequence for controlling spacecraft thruster power stages:
 * OFF -> SELF_TEST -> PREHEAT -> DISCHARGE_START -> NEUTRALIZER_START -> BEAM_RAMP -> THRUST -> SHUTDOWN
 */

#include <iostream>
#include <string>
#include <thread>
#include <chrono>

// Define all 8 operational states of the PPU state machine
enum class PPUState {
    OFF,                // System isolated and unpowered
    SELF_TEST,          // Check internal voltage, current, and temperature sensors
    PREHEAT,            // Apply heater power to warm up cathodes
    DISCHARGE_START,    // Ignite low-voltage discharge chamber plasma
    NEUTRALIZER_START,  // Establish neutralizer electron emission
    BEAM_RAMP,          // Ramp high-voltage beam supply to target acceleration potential
    THRUST,             // Closed-loop steady-state propulsion operation
    SHUTDOWN            // Controlled sequencing down to a safe state
};

/**
 * @brief Converts state enum values into printable strings for logging/telemetry.
 * @param state The current PPUState.
 * @return std::string Human-readable state identifier.
 */
std::string stateToString(PPUState state) {
    switch (state) {
        case PPUState::OFF:               return "OFF";
        case PPUState::SELF_TEST:         return "SELF_TEST";
        case PPUState::PREHEAT:           return "PREHEAT";
        case PPUState::DISCHARGE_START:   return "DISCHARGE_START";
        case PPUState::NEUTRALIZER_START: return "NEUTRALIZER_START";
        case PPUState::BEAM_RAMP:         return "BEAM_RAMP";
        case PPUState::THRUST:            return "THRUST";
        case PPUState::SHUTDOWN:          return "SHUTDOWN";
        default:                          return "UNKNOWN";
    }
}

/**
 * @class PPUController
 * @brief Manages PPU operational state transitions and channel sequencing.
 */
class PPUController {
private:
    PPUState currentState;  // Stores current operating state
    float throttle;         // Throttle level scaled from 0.0 (0%) to 1.0 (100%)

public:
    /**
     * @brief Constructor: Initializes controller in safe OFF state with 0% throttle.
     */
    PPUController() : currentState(PPUState::OFF), throttle(0.0f) {}

    /**
     * @brief Getter for the active state.
     */
    PPUState getState() const { return currentState; }

    /**
     * @brief Handles explicit state transitions and logs output.
     * @param newState Target state to transition into.
     */
    void transitionTo(PPUState newState) {
        std::cout << "[STATE TRANSITION] " << stateToString(currentState) 
                  << " -> " << stateToString(newState) << std::endl;
        currentState = newState;
    }

    /**
     * @brief Executes the full nominal startup, steady-state, and shutdown sequence.
     */
    void runSequence() {
        // Step 1: Execute built-in self-test diagnostics
        transitionTo(PPUState::SELF_TEST);
        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        // Step 2: Preheat thruster cathode filaments
        transitionTo(PPUState::PREHEAT);
        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        // Step 3: Start discharge power supply (Ignite plasma)
        transitionTo(PPUState::DISCHARGE_START);
        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        // Step 4: Start neutralizer supply (Charge neutralization)
        transitionTo(PPUState::NEUTRALIZER_START);
        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        // Step 5: Ramp high-voltage beam supply (Ion acceleration)
        transitionTo(PPUState::BEAM_RAMP);
        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        // Step 6: Enter steady-state nominal thrusting at 100% throttle
        transitionTo(PPUState::THRUST);
        throttle = 1.0f;
        std::cout << "[INFO] PPU Operating in Steady State THRUST at " 
                  << (throttle * 100.0f) << "% Throttle." << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));

        // Step 7: Begin commanded shutdown sequence
        transitionTo(PPUState::SHUTDOWN);
        throttle = 0.0f;
        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        // Step 8: Safely isolate all channels and return to OFF
        transitionTo(PPUState::OFF);
    }
};

int main() {
    std::cout << "--- Initializing Ion Propulsion PPU Controller ---" << std::endl;
    
    // Instantiate and execute controller state machine
    PPUController controller;
    controller.runSequence();
    
    std::cout << "--- PPU State Machine Test Complete ---" << std::endl;
    return 0;
}