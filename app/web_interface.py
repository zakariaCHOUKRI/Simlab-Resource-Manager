import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
from app.slurm_commands import run_sinfo_command, run_squeue_command
from app.data_processing import process_partition_data
import subprocess
import pandas as pd
import numpy as np

# Get partition information when the app starts
partition_data = run_sinfo_command("%P|%C|%G")
df_partitions = process_partition_data(partition_data)
df_partitions = df_partitions.loc[df_partitions["AvailableGPUs"] != "(null)"]

# Maximum allocation details for each partition
# We got this information from the official
# Simlab github documentation repository
max_allocation_details = {
    'defq*': {'MaxCpuTime': '1 hour', 'NodesAvailable': '7 (node[01-05], node14, node15)', 'MaxNodesPerJob': 1, 'MinMaxCoresPerJob': '1-44'},
    'shortq': {'MaxCpuTime': '4 hours', 'NodesAvailable': '7 (node[01-05], node14, node15)', 'MaxNodesPerJob': 2, 'MinMaxCoresPerJob': '1-88'},
    'longq': {'MaxCpuTime': '30 days', 'NodesAvailable': '7 (node[01-05], node14, node15)', 'MaxNodesPerJob': 1, 'MinMaxCoresPerJob': '1-44'},
    'special': {'MaxCpuTime': '30 minutes', 'NodesAvailable': '17 (all nodes)', 'MaxNodesPerJob': 17, 'MinMaxCoresPerJob': '1-740'},
    'visu': {'MaxCpuTime': '24 hours', 'NodesAvailable': '1 (visu01)', 'MaxNodesPerJob': 1, 'MinMaxCoresPerJob': '1-44'},
    'gpu': {'MaxCpuTime': '48 hours', 'NodesAvailable': '12 (node[06-17])', 'MaxNodesPerJob': 2, 'MinMaxCoresPerJob': '1-88'},
}

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

# Print the resulting DataFrame
# print(df)

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

# Group by 'Partition' and sum the 'GPU_Available' values
result_df = merged_df.groupby('Partition')['GPU_Available'].sum().reset_index()

# Fill NaN values with 0
result_df['GPU_Available'] = result_df['GPU_Available'].fillna(0).astype(int)

# Print the resulting DataFrame
gpu_information_df = result_df
gpu_information_df.loc[gpu_information_df['Partition'] == 'defq', 'Partition'] = 'defq*'

# Merge the two DataFrames based on the 'Nodes' column
merged_df2 = pd.merge(df1_exploded, df, left_on='Nodes', right_on='Node', how='left')

# Group by 'Partition' and aggregate the 'Node' and 'GPU_Available' values into lists
result_df2 = merged_df2.groupby('Partition').agg({'Nodes': list, 'GPU_Available': 'sum'}).reset_index()

# Fill NaN values with empty lists
result_df2['Nodes'] = result_df2['Nodes'].fillna('').apply(lambda x: x if isinstance(x, list) else [])

# Print the resulting DataFrame
gpu_information_df2 = result_df2
gpu_information_df2.loc[gpu_information_df2['Partition'] == 'defq', 'Partition'] = 'defq*'

# Filter out 'Partition' from the options and set it as the initial value
options = [{'label': partition, 'value': partition, 'disabled': partition.lower() == 'partition'} for partition in df_partitions['Partition']]
initial_value = options[0]['value']

app = dash.Dash(__name__)

app.layout = html.Div([

    html.Div([
        html.H1('Welcome To Simlab Resource Manager',
        style={'font-family': 'Trebuchet MS', 'text-align': 'center'}),
    ],
    style={'margin-bottom': '40px', 'padding': '24px', 'background': '#f5f5f5'}
    ),

    html.Div([
        html.Div([
            html.Label('Select Partition:',
            style={'font-size': '16px', 'font-family': 'Trebuchet MS'}
            ),
            dcc.Dropdown(
                id='partition-dropdown',
                options=options,
                value=initial_value,
                style={'font-size': '16px', 'width': '400px', 'margin-bottom': '20px', 'font-family': 'Trebuchet MS'}
            ),
        ]),
        
        html.Div([
            
            html.Div([
                html.H3(
                    'Information about this partition\'s CPUS',
                    style={'font-family': 'Trebuchet MS'}
                ),

                html.Div([
                    # Display the resource information in a table
                    dash_table.DataTable(
                        id='resource-table',
                        columns=[
                            {"name": "Metric", "id": "Metric"},
                            {"name": "Value", "id": "Value"},
                        ],
                        style_table={'overflowX': 'auto', 'font-size': '20px', 'font-family': 'Trebuchet MS', 'margin-bottom': '20px', 'width': '400px'},
                        style_header={'font-size': '22px', 'fontWeight': 'bold', 'padding': '10px', 'width': '200px', 'font-family': 'Trebuchet MS', 'text-align': 'center'},
                        style_cell={'padding': '10px', 'width': '200px', 'font-family': 'Trebuchet MS', 'text-align': 'center'}
                    ),
                ]),
            ]),
            
            html.Div([
                html.H3(
                    'Jobs running on this partition',
                    style={'font-family': 'Trebuchet MS'}
                ),
                html.Div([
                # Display the job information in a DataTable
                dash_table.DataTable(
                    id='table',
                    columns=[
                        {"name": col, "id": col} for col in ["JOBID", "PARTITION", "NAME", "USER", "ST", "NODES", "NODELIST(REASON)"]
                    ],
                    style_table={'overflowX': 'auto', 'font-size': '16px', 'font-family': 'Trebuchet MS', 'margin-bottom': '20px', 'width': '1400px'},
                    style_header={'font-size': '18px', 'fontWeight': 'bold', 'padding': '10px', 'header_repeated': False, 'width': '200px', 'font-family': 'Trebuchet MS', 'width': '400px', 'text-align': 'center'},
                    style_cell={'padding': '0px', 'font-family': 'Trebuchet MS', 'width': '200px', 'text-align': 'center'}
                    ),
                ]),
            ]),
            
        ],
        style={'display': 'flex', 'justify-content': 'space-between'}
        ),

        # Display maximum allocation details
        html.Div(
            id='max-allocation-info1',
            style={'margin-top': '20px', 'font-size': '24px', 'font-family': 'Trebuchet MS'}
        ),

        # Display maximum allocation details
        html.Div(
            id='max-allocation-info2',
            style={'margin-top': '20px', 'font-size': '24px', 'font-family': 'Trebuchet MS'}
        ),
    ]),

],)

@app.callback(
    [Output('resource-table', 'data'),
     Output('table', 'data'),
     Output('max-allocation-info1', 'children'),
     Output('max-allocation-info2', 'children')],
    [Input('partition-dropdown', 'value')]
)
def update_display(selected_partition):
    # Update DataTable for jobs
    squeue_output = run_squeue_command(selected_partition)
    lines = squeue_output.split('\n')
    header = lines[0].split()
    job_rows = [dict(zip(header, line.split())) for line in lines[1:] if line]

    # Update DataTable for resource information
    selected_partition_info = df_partitions[df_partitions['Partition'] == selected_partition]

    # Get the list of nodes with available GPUs
    gpu_nodes = gpu_information_df2[gpu_information_df2['Partition'] == selected_partition]['Nodes'].values
    gpu_nodes_str = ', '.join(set(map(str, gpu_nodes[0]))) if gpu_nodes and gpu_nodes[0] else 'N/A'

    if not selected_partition_info.empty:
        # Check if the columns exist and remove leading/trailing whitespaces
        selected_partition_info.columns = selected_partition_info.columns.str.strip()
        if 'AvailableCPUs' in selected_partition_info.columns and 'AvailableGPUs' in selected_partition_info.columns:
            available_cpus_values = selected_partition_info['AvailableCPUs'].values[0].split('/')
            resource_data = [
                {"Metric": "Partition", "Value": selected_partition_info['Partition'].values[0]},
                {"Metric": "Allocated", "Value": available_cpus_values[0]},
                {"Metric": "Idle", "Value": available_cpus_values[1]},
                {"Metric": "Other", "Value": available_cpus_values[2]},
                {"Metric": "Total", "Value": available_cpus_values[3]}
            ]

            # Fetch GPU information from gpu_information_df DataFrame
            gpu_info_row = gpu_information_df[gpu_information_df['Partition'] == selected_partition]
            if not gpu_info_row.empty:
                gpu_info_value = gpu_info_row['GPU_Available'].values[0]
                resource_data.append({"Metric": "Available GPUs", "Value": (len(gpu_nodes_str)+2)//8})
        else:
            resource_data = []

        # Get maximum allocation details
        max_allocation = max_allocation_details.get(selected_partition, {})
        la_variable = max_allocation.get('MinMaxCoresPerJob', 'N/A')
        if "-" in la_variable:
            la_variable2 = la_variable.split("-")
            la_variable3 = int(la_variable2[1])
            la_variable4 = min(la_variable3, int(available_cpus_values[1]))
        else:
            la_variable4 = "N/A"
        
        max_allocation_info1 = [
            f"The number of CPUs You Can Allocate: {la_variable4}",
        ]
        max_allocation_info2 = [
            f"Nodes with available GPU are: {gpu_nodes_str}",
        ]
    else:
        resource_data = []
        max_allocation_info1 = []
        max_allocation_info2 = []

    return resource_data, job_rows, max_allocation_info1, max_allocation_info2

if __name__ == '__main__':
    app.run_server(debug=True)
