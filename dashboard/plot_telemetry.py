"""
@file plot_telemetry.py
@brief Telemetry Data Visualization & Analytics Engine for Spacecraft PPU

This script ingests historical operational data from the CSV telemetry log,
parses time-series performance metrics, and renders a dual-axis plot comparing
output power against conversion efficiency over time.
"""

import csv
import matplotlib.pyplot as plt

def plot_logs(log_file="dashboard/telemetry_log.csv"):
    """
    @brief Reads logged telemetry data and outputs a dual-axis trend graph.
    @param log_file Filepath to the CSV telemetry source log.
    """
    # Time-series storage lists for telemetry axes
    timestamps = []
    p_out_list = []
    efficiency_list = []

    try:
        # Open CSV log file in read-only mode
        with open(log_file, mode='r') as f:
            # Use DictReader to automatically parse header columns into key-value pairs
            reader = csv.DictReader(f)
            
            # Iterate through recorded telemetry rows and extract metrics
            for row in reader:
                timestamps.append(row["timestamp"])
                p_out_list.append(float(row["p_out"]))
                efficiency_list.append(float(row["efficiency"]))

        print(f"[INFO] Successfully parsed {len(timestamps)} log entries from {log_file}.")
        
        # Instantiate Matplotlib figure and primary axis (Left Y-Axis: Power)
        fig, ax1 = plt.subplots(figsize=(10, 5))
        
        # Configure primary X and Y axis labels and styles
        ax1.set_xlabel('Sample / Timestamp Index')
        ax1.set_ylabel('Output Power (W)', color='tab:blue')
        ax1.plot(p_out_list, color='tab:blue', linewidth=2, label='Output Power (W)')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        ax1.grid(True, linestyle='--', alpha=0.5)

        # Create twin axis sharing the same X-axis (Right Y-Axis: Efficiency)
        ax2 = ax1.twinx()
        ax2.set_ylabel('System Efficiency (%)', color='tab:green')
        ax2.plot(efficiency_list, color='tab:green', linestyle='--', linewidth=2, label='Efficiency (%)')
        ax2.tick_params(axis='y', labelcolor='tab:green')
        
        # Enforce realistic percentage bounds for efficiency Y-axis
        ax2.set_ylim(0, 100)

        # Apply chart layout metadata and save high-resolution figure
        plt.title('PPU Dynamic Telemetry Performance Profile')
        plt.tight_layout()
        plt.savefig("dashboard/telemetry_plot.png", dpi=300)
        
        print("[SUCCESS] Waveform plot rendered and saved to dashboard/telemetry_plot.png")

    except FileNotFoundError:
        print(f"[ERROR] Telemetry log file '{log_file}' not found. Run app.py first to generate data!")
    except Exception as e:
        print(f"[ERROR] An error occurred while parsing telemetry data: {e}")

if __name__ == "__main__":
    # Execute visualization engine against default log path
    plot_logs()