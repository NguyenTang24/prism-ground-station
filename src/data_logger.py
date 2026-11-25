import csv
import os
from datetime import datetime

class DataLogger:
    def __init__(self, output_dir="data"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Create a timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filepath = os.path.join(self.output_dir, f"prism_flight_{timestamp}.csv")
        
        # Initialize the CSV file with headers
        with open(self.filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp_ms", "pressure_pa", "raw1", "raw2", "batt_mv"])

    def log_data(self, data_string):
        """Appends a single parsed data row to the CSV."""
        # data_string is expected to be "timestamp,pressure,raw1,raw2,batt"
        with open(self.filepath, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data_string.split(','))