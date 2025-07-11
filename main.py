import pandas as pd
from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px

# test commit
def main():
    # pulling in the data
    df1 = pd.read_csv('Endpoint.csv')
    df2 = pd.read_csv('Identity.csv')
    df3 = pd.read_csv('Network.csv')
    df4 = pd.read_excel('Web.xlsx')
    df5 = pd.read_csv('Incidents.csv')
    app = Dash()

    app.layout = html.Div([
        html.H1("pre-before-antes-Alpha"),
        dcc.Tabs([
            dcc.Tab(label='F1', children=[
                html.H2("Endpoint Data"),
                dcc.Graph(
                    id='endpoint-graph',
                    figure=px.histogram(df1, x=df1.columns[2])  # Change x= to a relevant column
                ),
                html.Div([
                    html.H4("Endpoint Table"),
                    dcc.Markdown(df1.head().to_markdown())
                ]),
                html.H2("Identity Data"),
                dcc.Graph(
                    id='identity-graph',
                    figure=px.histogram(df2, x=df2.columns[0])  # Change x= to a relevant column
                ),
                html.Div([
                    html.H4("Identity Table"),
                    dcc.Markdown(df2.head().to_markdown())
                ]),
                html.H2("Web Data"),
                dcc.Graph(
                    id='web-graph',
                    figure=px.histogram(df4, x=df4.columns[0])  # Change x= to a relevant column
                ),
                html.Div([
                    html.H4("Web Table"),
                    dcc.Markdown(df4.head().to_markdown())
                ])
            ]),
            dcc.Tab(label='F2', children=[
                html.H2("Identity Data"),
                dcc.Graph(
                    id='identity-graph',
                    figure=px.histogram(df2, x=df2.columns[0])  # Change x= to a relevant column
                ),
                html.Div([
                    html.H4("Identity Table"),
                    dcc.Markdown(df2.head().to_markdown())
                ])
            ]),
            dcc.Tab(label='F3', children=[
                html.H2("Web Data"),
                dcc.Graph(
                    id='web-graph',
                    figure=px.histogram(df4, x=df4.columns[0])  # Change x= to a relevant column
                ),
                html.Div([
                    html.H4("Web Table"),
                    dcc.Markdown(df4.head().to_markdown())
                ])
            ]),
        ])
    ])

    app.run(debug=True)

if __name__ == "__main__":
    main()

    
