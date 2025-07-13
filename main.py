import pandas as pd
from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
from datetime import datetime

# test commit
def main():
    # pulling in the data
    df1 = pd.read_csv('Endpoint.csv')
    df2 = pd.read_csv('Identity.csv')
    df3 = pd.read_csv('Network.csv')
    df4 = pd.read_excel('Web.xlsx')
    df5 = pd.read_csv('Incidents.csv')
    df11 = df1
    df22 = df2
    df44 = df4
    for n, row in df1.iterrows():
        a = datetime.strptime(row['detection_time'], '%Y-%m-%dT%H:%M:%S')
        if a < datetime.strptime('2025-06-20 00:00:00', '%Y-%m-%d %H:%M:%S'):
            df11.drop(n, inplace=True)
    for n, row in df2.iterrows():
        a = datetime.strptime(row['login_timestamp'], '%Y-%m-%dT%H:%M:%S')
        if a < datetime.strptime('2025-06-20 00:00:00', '%Y-%m-%d %H:%M:%S'):
            df22.drop(n, inplace=True)
    for n, row in df4.iterrows():
        a = datetime.strptime(row['timestamp'], '%Y-%m-%dT%H:%M:%S.%f')
        if a < datetime.strptime('2025-06-20 00:00:00', '%Y-%m-%d %H:%M:%S'):
            df44.drop(n, inplace=True)
    app = Dash()

    app.layout = html.Div([
        html.H1("Security Dashboard"),
        dcc.Tabs([
            dcc.Tab(label = 'The Present', children = [
                html.H2("Endpoint Data"),
                dcc.Graph(
                    id = 'endpoint-graph1',
                    figure = px.bar(
                        df11['threat_type'].value_counts().reset_index(),
                        x = df11['threat_type'].value_counts().reset_index().index,
                        y = 'threat_type',
                        title = 'Most Common Types of Malware Detected',
                        labels = {'index': 'Malware Type', 'threat_type': 'Count'},
                        color = 'threat_type',
                        color_discrete_sequence = px.colors.qualitative.Set3
                    ).update_layout(
                        xaxis_title = "Malware Type",
                        yaxis_title = "Number of Detections",
                        showlegend=False
                    )
                ),
                html.Div([
                    html.H4("Endpoint Table"),
                    dcc.Markdown(df11.head().to_markdown())
                ]),
                html.H2("Identity Data"),
                dcc.Graph(
                    id = 'identity-graph1',
                    figure = px.bar(
                        df22[df22['login_status'] == 'Failure']['username'].value_counts().reset_index(),
                        x = df22[df22['login_status'] == 'Failure']['username'].value_counts().reset_index().index,
                        y = 'username',
                        title = 'Users with Most Failed Login Attempts',
                        labels = {'index': 'Username', 'username': 'Failed Login Count'},
                        color = 'username',
                        color_discrete_sequence = px.colors.qualitative.Set1
                    ).update_layout(
                        xaxis_title = "Username",
                        yaxis_title = "Number of Failed Logins",
                        showlegend = False
                    )
                ),
                html.Div([
                    html.H4("Identity Table"),
                    dcc.Markdown(df22.head().to_markdown())
                ]),
                html.H2("Web Data"),
                dcc.Graph(
                    id = 'web-graph1',
                    figure = px.bar(
                        df44['url_accessed'].value_counts().head(10).reset_index(),
                        x = df44['url_accessed'].value_counts().head(10).reset_index().index,
                        y = 'url_accessed',
                        title = 'Top 10 Most Accessed URLs on Server',
                        labels = {'index': 'URL', 'url_accessed': 'Access Count'},
                        color = 'url_accessed',
                        color_discrete_sequence = px.colors.qualitative.Pastel
                    ).update_layout(
                        xaxis_title = "URL",
                        yaxis_title = "Number of Accesses",
                        showlegend = False
                    )
                ),
                html.Div([
                    html.H4("Web Table"),
                    dcc.Markdown(df44.head().to_markdown())
                ])
            ]),
            dcc.Tab(label='The Past', children=[
                html.H2("Identity Data"),
                dcc.Graph(
                    id='identity-graph2',
                    figure=px.histogram(df2, x=df2.columns[0])  # Change x= to a relevant column
                ),
                html.Div([
                    html.H4("Identity Table"),
                    dcc.Markdown(df2.head().to_markdown())
                ])
            ]),
            dcc.Tab(label='The Future', children=[
                html.H2("Web Data"),
                dcc.Graph(
                    id='web-graph2',
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

    
