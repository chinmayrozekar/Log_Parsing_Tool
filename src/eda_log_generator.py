import os
import random
import time
from datetime import datetime

def generate_eda_line():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    phases = ["INIT", "LOAD", "PARSE", "ANALYSIS", "REPORT", "CLEANUP"]
    severities = ["INFO", "WARNING", "ERROR", "DEBUG", "FATAL"]
    
    phase = random.choice(phases)
    severity = random.choices(severities, weights=[70, 15, 10, 4, 1])[0]
    
    # Realistic EDA log patterns
    templates = [
        f"[{timestamp}] {severity} [{phase}] Processing design hierarchy: cell '{random.choice(['top_module', 'u_core', 'u_alu', 'u_mem_ctrl'])}' (depth {random.randint(1, 10)})",
        f"[{timestamp}] {severity} [{phase}] License checked out: {random.choice(['ADV_VLSI_CHECK', 'DRC_ENGINE', 'TIMING_PRO', 'LVS_PREMIUM'])}",
        f"[{timestamp}] {severity} [{phase}] Design rule violation at (X:{random.uniform(0, 1000):.3f}, Y:{random.uniform(0, 1000):.3f}) on layer {random.randint(1, 15)}",
        f"[{timestamp}] {severity} [{phase}] Peak memory usage: {random.randint(1024, 16384)} MB",
        f"[{timestamp}] {severity} [{phase}] Combinatorial loop detected through net 'net_{random.randint(1000, 9999)}'",
        f"[{timestamp}] {severity} [{phase}] Timing constraint unmet for path from '{random.choice(['reg_a', 'reg_b', 'clk_gate'])}' to '{random.choice(['out_0', 'mem_data_in'])}'",
        f"[{timestamp}] {severity} [{phase}] Parsing design file: '/usr/designs/src/{random.choice(['core.v', 'alu.v', 'mem.sv', 'top.vhd'])}' (lines: {random.randint(100, 50000)})",
        f"[{timestamp}] {severity} [{phase}] Unexpected error code 0x{random.randint(0, 0xFFFF):04X} during design flattening",
    ]
    
    return random.choice(templates) + "\n"

def create_eda_logs(file_path, target_size_mb):
    target_bytes = int(target_size_mb * 1024 * 1024)
    print(f"Starting generation of EDA-style log: {file_path}. Target: {target_size_mb} MB.")
    start_time = time.time()

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    bytes_written = 0
    
    with open(file_path, 'w') as f:
        # Tool Header
        f.write(f"--- EDA Tool Suite v2026.03 (Build {random.randint(100000, 999999)}) ---\n")
        f.write(f"--- Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        f.write(f"--- Host: {random.choice(['compute-01', 'eda-srv-05', 'mac-m4-pro'])} ---\n\n")
        
        while bytes_written < target_bytes:
            chunk = [generate_eda_line() for _ in range(5000)]
            chunk_str = "".join(chunk)
            f.write(chunk_str)
            bytes_written += len(chunk_str.encode('utf-8'))
            
    end_time = time.time()
    print(f"Generation complete. Took {round(end_time - start_time, 2)} seconds. File: {file_path}")

if __name__ == "__main__":
    create_eda_logs("data/raw_logs/eda_sim_50mb.log", 50)
