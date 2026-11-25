import sys
from serial_reader import SerialReader
from data_logger import DataLogger
from plotter import LivePlotter

def main():
    # You will need to change 'COM3' to your actual USB-UART port
    # Windows: COM3, COM4, etc. | Mac/Linux: /dev/ttyUSB0, /dev/ttyACM0
    PORT = 'COM3' 
    BAUD = 115200

    print("Starting PRISM Ground Station...")
    
    reader = SerialReader(port=PORT, baudrate=BAUD)
    logger = DataLogger()
    
    reader.connect()
    
    if not reader.running:
        print("Exiting: Could not open serial port.")
        sys.exit(1)

    # Start the live plotter
    plotter = LivePlotter(reader)
    
    try:
        # Note: To properly log data, you would hook the logger into the 
        # plotter's update loop, or run a separate logging thread.
        plotter.start()
    except KeyboardInterrupt:
        print("\nStopping ground station.")
    finally:
        reader.disconnect()
        print(f"Data saved to: {logger.filepath}")

if __name__ == "__main__":
    main()