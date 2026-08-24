Power Flow: 24 V Spacecraft Bus -> Input Filter & Protection Block -> 4 Parallel DC-DC Power Stages (Beam, Discharge, Neutralizer, Aux) -> Sensor Blocks (Voltage/Current Sensing) -> Output Connectors.  
Control & Telemetry Flow: Sensing Blocks -> C++ Controller Analog Inputs -> C++ State Machine Decisions -> PWM Gate Drivers / Channel Enable Switches.  
Software-in-the-Loop (SiL) Interface: C++ Controller Commands -> IPC Pipe/Socket Interface -> Python Dynamic Thruster Plant Model -> Real-time Ground Station Telemetry Dashboard.

# PPU PCB Layout & Stackup Specification

## Board Geometry & Layer Stackup
- **Dimensions:** 100 mm x 80 mm (Bench-scale footprint)
- **Layer Count:** 4-Layer Stackup
  - **Layer 1 (Top):** High-voltage signal traces, MOSFET switches, gate drivers
  - **Layer 2 (Inner 1):** Solid GND Plane (Analog & Digital Ground reference)
  - **Layer 3 (Inner 2):** 24V Power Bus & Low-Voltage Power Rails
  - **Layer 4 (Bottom):** Low-frequency control signals & MCU routing

## Isolation & Creepage Constraints
- **High-Voltage Zone:** 100V Beam Converter isolated from 5V/3.3V digital MCU logic.
- **Creepage / Clearance:** Minimum 1.5 mm clearance enforced between Beam output lines and low-voltage digital net traces.