from dash import html, dcc

def create_layout():
    layout = html.Div([
        html.H1("Slurm Cluster Resource Management", style={'textAlign': 'center'}),
        html.Div([
            html.Label("Select a Partition:", style={'fontSize': 20, 'marginRight': 10}),
            dcc.Dropdown(
                id='partition-dropdown',
                options=[],  # This will be populated dynamically via callback in app.py
                style={'width': '50%'}
            ),
        ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'marginTop': 20}),

        html.Div(id='cpu-gpu-info', style={'marginTop': 20, 'textAlign': 'center'})
    ], style={'padding': 40})

    return layout

# Assign the layout to a variable
layout = create_layout()
