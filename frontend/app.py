import dash
from dash import html
import callbacks  # Import the callbacks module
from layouts import layout  # Import the layout from layouts.py

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server  # Expose the server for potential deployment

# Set the app layout from layouts.py
app.layout = layout

# Register the callbacks from callbacks.py
callbacks.register_callbacks(app)

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)
