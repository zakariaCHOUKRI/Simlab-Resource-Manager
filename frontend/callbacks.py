from dash import Dash, dcc, html, Input, Output
import subprocess
import json

def register_callbacks(app: Dash):
    @app.callback(
        Output('partition-dropdown', 'options'),
        Output('cpu-gpu-info', 'children'),
        [Input('partition-dropdown', 'value')]
    )
    def update_partition_info(selected_partition):
        # Call the backend script and get data
        result = subprocess.run(['python3', '../backend/infos_parser.py'], stdout=subprocess.PIPE)
        data = json.loads(result.stdout.decode('utf-8'))

        # Update partition dropdown options
        partitions = data.get("sinfo", {}).get("partitions", [])
        partition_options = [{"label": p, "value": p} for p in partitions]

        # Update CPU/GPU info based on the selected partition
        cpu_gpu_info = ""
        if selected_partition:
            cpu_gpu_info = data.get("scontrol", {}).get(selected_partition, "No data available")

        return partition_options, html.Div(str(cpu_gpu_info))

