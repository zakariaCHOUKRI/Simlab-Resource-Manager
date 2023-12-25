import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
from app.slurm_commands import run_sinfo_command, run_squeue_command
from app.data_processing import process_partition_data
import subprocess
import pandas as pd
import numpy as np


def run_gpu_command():
    script_path = 'gpu_script.sh'
    result = subprocess.run(['bash', script_path], capture_output=True, text=True)

    # Split the lines of the output
    lines = result.stdout.strip().split('\n')

    # Split each line into columns
    data = [line.split()[:2] for line in lines]

    # Create a Pandas DataFrame
    columns = ['Node', 'GPU_Available']
    df = pd.DataFrame(data, columns=columns)

    # Convert 'GPU_Available' column to integers
    df['GPU_Available'] = df['GPU_Available'].astype(int)

    return df

# Call the function
df = run_gpu_command()

# Define the data
data1 = {
    'Partition': ['defq', 'shortq', 'longq', 'special', 'visu', 'gpu'],
    'Nodes': [np.nan,
              np.nan,
              np.nan,
              np.nan,
              np.nan,
              'node06, node07, node08, node09, node10, node11, node12, node13, node15, node16, node17']
}

# Create a Pandas DataFrame
df1 = pd.DataFrame(data1)

# Split the comma-separated nodes into a list
df1['Nodes'] = df1['Nodes'].apply(lambda x: str(x).split(', ') if pd.notna(x) else [])

# Explode the list of nodes into separate rows
df1_exploded = df1.explode('Nodes')

# Merge the two DataFrames based on the 'Nodes' column
merged_df = pd.merge(df1_exploded, df, left_on='Nodes', right_on='Node', how='left')

# Group by 'Partition' and aggregate the 'Node' and 'GPU_Available' values into lists
result_df = merged_df.groupby('Partition').agg({'Nodes': list, 'GPU_Available': 'sum'}).reset_index()

# Fill NaN values with empty lists
result_df['Nodes'] = result_df['Nodes'].fillna('').apply(lambda x: x if isinstance(x, list) else [])

# Print the resulting DataFrame
gpu_information_df = result_df
gpu_information_df.loc[gpu_information_df['Partition'] == 'defq', 'Partition'] = 'defq*'
print(gpu_information_df)