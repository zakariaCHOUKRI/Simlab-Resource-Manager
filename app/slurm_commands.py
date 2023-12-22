import subprocess

def run_sinfo_command(format_string):
    command = ['sinfo', f'--format={format_string}']
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def run_squeue_command(partition=None):
    command = ['squeue']
    if partition:
        command.extend(['-p', partition])
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()