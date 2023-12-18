# data_processing.py
import subprocess
import pandas as pd

def run_slurm_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def get_partition_info():
    command = ['sinfo', '--format=%P|%C|%G']
    partition_data = run_slurm_command(command)
    return partition_data

def process_partition_data(partition_data):
    columns = ['Partition', 'AvailableCPUs', 'AvailableGPUs']
    data = [line.split('|') for line in partition_data.split('\n')]
    df = pd.DataFrame(data, columns=columns)
    # Additional data processing if needed
    return df
