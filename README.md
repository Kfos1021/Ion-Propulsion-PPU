**Spacecraft Ion Propulsion Power Processing Unit**

This Ion Propulsion Power Processing Unit (PPU) is a simulation-first hardware and embedded software project 
that converts a standard 24 V DC spacecraft bus into four independently regulated power stages: a 50–100 V Boost/Flyback 
Beam supply, a 12–24 V Discharge supply, a 5–12 V Neutralizer supply, and a 5–12 V Auxiliary supply. The architecture 
integrates closed-loop LTspice circuit modeling, a 8-state bare-metal C++ safety state machine with active hardware interlocks, 
a Python dynamic thruster load simulator with a Software-in-the-Loop (SiL) socket interface, and a fully routed 2-layer KiCad 
PCB layout validated to a Design Rule Check (DRC) pass.

<img width="1278" height="628" alt="ppu_3d_render" src="https://github.com/user-attachments/assets/2f1f2ed5-c9e6-434b-a06b-df431e46cd9b" />

**3D View of PPU**
