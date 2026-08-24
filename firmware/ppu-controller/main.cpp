/**
 * @file main.cpp
 * @brief Bare-Metal C++ PPU Controller with Safety Interlocks & Fault Logic
 */

#include <iostream>
#include <string>
#include <thread>
#include <chrono>

// Define all 8 operational states
enum class PPUState {
    OFF,
    SELF_TEST,
    PREHEAT,
    DISCHARGE_START,
    NEUTRALIZER_START,
    BEAM_RAMP,
    THRUST,
    SHUTDOWN
};

// Hardware status telemetry structure
struct Telemetry {
    float busVoltage = 24.0f;     // Nominal 24V DC bus
    float dischargeCurrent = 1.2f;// Nominal discharge current (Amps)
    float neutralizerCurrent = 0.5f; // Nominal neutralizer current (Amps)
    float beamCurrent = 0.2f;     // Beam current (Amps)
    float temperature = 45.0f;    // PPU board temperature (°C)
};

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

class PPUController {
private:
    PPUState currentState;
    Telemetry telem;
    float throttle;
    int faultRetries;
    const int MAX_RETRIES = 3;

public:
    PPUController() : currentState(PPUState::OFF), throttle(0.0f), faultRetries(0) {}

    void transitionTo(PPUState newState) {
        std::cout << "[STATE TRANSITION] " << stateToString(currentState) 
                  << " -> " << stateToString(newState) << std::endl;
        currentState = newState;
    }

    /**
     * @brief Evaluates active safety interlocks before enabling high-voltage stages.
     */
    bool checkInterlocks() {
        // Interlock 1: Spacecraft Bus Undervoltage (<18V)
        if (telem.busVoltage < 18.0f) {
            std::cout << "[FAULT ERROR] Bus Undervoltage Detected: " << telem.busVoltage << "V!" << std::endl;
            return false;
        }

        // Interlock 2: Thermal Cutoff (>85°C)
        if (telem.temperature > 85.0f) {
            std::cout << "[FAULT ERROR] Overtemperature Trip: " << telem.temperature << "°C!" << std::endl;
            return false;
        }

        // Interlock 3: High-Voltage Beam Interlock
        // Prohibit beam activation if discharge or neutralizer plasma isn't established
        if (currentState == PPUState::BEAM_RAMP || currentState == PPUState::THRUST) {
            if (telem.dischargeCurrent < 0.5f || telem.neutralizerCurrent < 0.1f) {
                std::cout << "[INTERLOCK TRIP] Cannot enable Beam supply without active Discharge & Neutralizer!" << std::endl;
                return false;
            }
        }
        return true;
    }

    /**
     * @brief Handles system fault response, immediate shutdown, and latched lockdown.
     */
    void handleFault(const std::string& errorReason) {
        std::cout << "\n[EMERGENCY SHUTDOWN] Fault Triggered: " << errorReason << std::endl;
        transitionTo(PPUState::SHUTDOWN);
        throttle = 0.0f;
        
        faultRetries++;
        std::cout << "[RECOVERY] Retries attempted: " << faultRetries << " / " << MAX_RETRIES << std::endl;
        
        if (faultRetries >= MAX_RETRIES) {
            std::cout << "[CRITICAL LOCKDOWN] Max fault retries exceeded. System latched in OFF state." << std::endl;
            transitionTo(PPUState::OFF);
        } else {
            std::cout << "[RECOVERY] Clearing faults and resetting to OFF for retry..." << std::endl;
            transitionTo(PPUState::OFF);
        }
    }

    void runNominalAndFaultTest() {
        std::cout << "\n--- TEST 1: Nominal Startup & Interlock Check ---" << std::endl;
        transitionTo(PPUState::SELF_TEST);
        if (!checkInterlocks()) { handleFault("Self-Test Interlock Failed"); return; }

        transitionTo(PPUState::PREHEAT);
        transitionTo(PPUState::DISCHARGE_START);
        transitionTo(PPUState::NEUTRALIZER_START);

        // Verify beam interlock passes now that discharge and neutralizer currents are nominal
        if (checkInterlocks()) {
            transitionTo(PPUState::BEAM_RAMP);
            transitionTo(PPUState::THRUST);
            throttle = 1.0f;
            std::cout << "[INFO] THRUST Active at 100% Throttle." << std::endl;
        }

        std::cout << "\n--- TEST 2: Injecting Beam Arc Overcurrent Fault ---" << std::endl;
        // Inject dynamic fault: Sudden neutralizer failure while operating
        telem.neutralizerCurrent = 0.0f; 
        if (!checkInterlocks()) {
            handleFault("Neutralizer Current Lost during THRUST");
        }
    }
};

int main() {
    std::cout << "--- Initializing PPU Interlocks & Protection System ---" << std::endl;
    PPUController controller;
    controller.runNominalAndFaultTest();
    std::cout << "--- Day 12 Interlocks & Protection Test Complete ---" << std::endl;
    return 0;
}