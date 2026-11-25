import serial
import threading
import queue
import time

class SerialReader:
    def __init__(self, port='COM3', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.running = False
        self.data_queue = queue.Queue(maxsize=64) # 64-record ring buffer

    def connect(self):
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"Connected to {self.port} at {self.baudrate} baud.")
            self.running = True
            self.thread = threading.Thread(target=self._read_loop, daemon=True)
            self.thread.start()
        except serial.SerialException as e:
            print(f"Failed to connect to {self.port}: {e}")

    def _read_loop(self):
        while self.running:
            try:
                # Read a line terminated by \n
                line = self.serial_conn.readline().decode('ascii').strip()
                if line:
                    # Example expected format: timestamp_ms,pressure_pa,raw1,raw2,batt_mv
                    if self.data_queue.full():
                        self.data_queue.get() # Drop oldest if buffer is full
                    self.data_queue.put(line)
            except Exception as e:
                print(f"Serial read error: {e}")
                time.sleep(0.1)

    def disconnect(self):
        self.running = False
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Serial connection closed.")