from dash import Dash, dcc

app = Dash(__name__)

app.layout = dcc.RadioItems(['New York City', 'Montreal','San Francisco'], 'Montreal')

if __name__ == "__main__":
    app.run(debug=True)
