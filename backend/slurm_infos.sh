#!/bin/bash

# Define paths for temporary files
sinfo_output_file="/tmp/sinfo_output.txt"
squeue_output_file="/tmp/squeue_output.txt"
scontrol_output_file="/tmp/scontrol_output.txt"

# Fetch data using Slurm commands
# sinfo for viewing information about Slurm nodes and partitions
# squeue for viewing information about jobs in the queue
# scontrol for detailed information about nodes and other configurations

# Fetch and store sinfo output
sinfo > "$sinfo_output_file"

# Fetch and store squeue output
squeue > "$squeue_output_file"

# Fetch and store scontrol output
scontrol show node > "$scontrol_output_file"

# Optional: Echo paths of output files for logging or debugging
echo "sinfo output stored in: $sinfo_output_file"
echo "squeue output stored in: $squeue_output_file"
echo "scontrol output stored in: $scontrol_output_file"

# End of script
