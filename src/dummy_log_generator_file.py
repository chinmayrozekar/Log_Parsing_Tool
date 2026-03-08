import os
import random
import time
from datetime import datetime

def generate_line():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
    components = ["CORE", "NETWORK", "DISK", "MEMORY", "AUTH", "API"]
    
    level = random.choices(levels, weights=[70, 15, 10, 5])[0]
    component = random.choice(components)
    
    # Diverse log templates
    templates = [
        f"[{timestamp}] {level} [{component}] Connection established from 192.168.1.{random.randint(1, 255)}",
        f"[{timestamp}] {level} [{component}] Task {random.randint(1000, 9999)} completed in {random.uniform(0.1, 5.0):.2f}s",
        f"[{timestamp}] {level} [{component}] Unexpected error code 0x{random.randint(0, 0xFFFF):04X} encountered",
        f"[{timestamp}] {level} [{component}] User {random.randint(100, 999)} logged in via {random.choice(['SSH', 'WEB', 'API'])}",
        f"[{timestamp}] {level} [{component}] Failed to write to block {random.randint(0, 0xFFFFFF):08X}",
        f"[{timestamp}] {level} [{component}] Memory usage spiked to {random.randint(70, 99)}%",
    ]
    
    return random.choice(templates) + "\n"

def create_dummy_logs(file_path, target_size_mb):
    target_bytes = int(target_size_mb * 1024 * 1024)
    print(f"Starting generation of {file_path}. Target size: {target_size_mb} MB.")
    start_time = time.time()

    bytes_written = 0
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w') as f:
        while bytes_written < target_bytes:
            chunk = []
            # Generate 5,000 lines at a time
            for _ in range(5000):
                line = generate_line()
                chunk.append(line)
            
            chunk_str = "".join(chunk)
            f.write(chunk_str)
            bytes_written += len(chunk_str.encode('utf-8'))
            
    end_time = time.time()
    print(f"Generation complete. Took {round(end_time - start_time, 2)} seconds. File: {file_path}")

if __name__ == "__main__":
    # Generate a 10MB log file for testing
    create_dummy_logs("data/raw_logs/system_test.log", 10)