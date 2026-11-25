import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

class LivePlotter:
    def __init__(self, serial_reader):
        self.serial_reader = serial_reader
        
        # Store the last 100 data points for the rolling plot
        self.timestamps = deque(maxlen=100)
        self.pressures = deque(maxlen=100)
        self.battery = deque(maxlen=100)

        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 6))
        self.fig.suptitle('PRISM Live Flight Data')

        # Setup Pressure Plot
        self.line_press, = self.ax1.plot([], [], 'b-', label='Pressure (Pa)')
        self.ax1.set_ylabel('Pressure (Pa)')
        self.ax1.set_xlabel('Time (ms)')
        self.ax1.legend(loc='upper right')

        # Setup Battery Plot
        self.line_batt, = self.ax2.plot([], [], 'r-', label='Battery (mV)')
        self.ax2.set_ylabel('Battery (mV)')
        self.ax2.set_xlabel('Time (ms)')
        self.ax2.legend(loc='upper right')

    def update_plot(self, frame):
        # Drain the queue from the serial reader
        while not self.serial_reader.data_queue.empty():
            line = self.serial_reader.data_queue.get()
            try:
                parts = line.split(',')
                if len(parts) >= 5:
                    t = int(parts[0])
                    p = float(parts[1])
                    b = int(parts[4])
                    
                    self.timestamps.append(t)
                    self.pressures.append(p)
                    self.battery.append(b)
            except ValueError:
                pass # Ignore malformed lines

        if self.timestamps:
            self.line_press.set_data(self.timestamps, self.pressures)
            self.line_batt.set_data(self.timestamps, self.battery)

            # Auto-scale axes
            self.ax1.relim()
            self.ax1.autoscale_view()
            self.ax2.relim()
            self.ax2.autoscale_view()

        return self.line_press, self.line_batt

    def start(self):
        self.ani = animation.FuncAnimation(
            self.fig, self.update_plot, interval=100, blit=False
        )
        plt.tight_layout()
        plt.show()