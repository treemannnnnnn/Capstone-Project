import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
from datetime import datetime

def main():

    df1 = pd.read_csv('Endpoint.csv')
    df2 = pd.read_csv('Identity.csv')
    df3 = pd.read_csv('Network.csv')
    df4 = pd.read_excel('Web.xlsx')
    df5 = pd.read_csv('Incidents.csv')  

    df11 = df1.copy()
    df22 = df2.copy()
    df44 = df4.copy()

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

    
    df5['report_time'] = pd.to_datetime(df5['report_time'])
    df5['date'] = df5['report_time'].dt.date
    df5['hour'] = df5['report_time'].dt.hour

   
    heatmap_data = df5.groupby(['date', 'hour']).size().reset_index(name='count')
    heatmap_fig = px.density_heatmap(
        data_frame=heatmap_data,
        x='hour',
        y='date',
        z='count',
        nbinsx=24,
        color_continuous_scale='Viridis',
        title='Malware Detections by Date and Hour',
        labels={'hour': 'Hour of Day', 'date': 'Date', 'count': 'Detections'}
    )
    heatmap_fig.update_layout(height=600)

    
    severity_fig = px.histogram(
        df11,
        x='threat_type',
        color='severity',  
        barmode='stack',
        title='Threat Types by Severity',
        labels={'threat_type': 'Threat Type', 'severity': 'Severity Level'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    severity_fig.update_layout(
        xaxis_title='Threat Type',
        yaxis_title='Number of Incidents',
        legend_title='Severity'
    )

   
    F1 = html.Div([
        html.H3("The Past: Historical Malware Detections"),
        dcc.Graph(figure=heatmap_fig),
        html.H3("Threat Types by Severity"),
        dcc.Graph(figure=severity_fig)
    ])

    
    app = Dash()

    app.layout = html.Div([
        html.H1("Security Dashboard"),
        dcc.Tabs([
            dcc.Tab(label='The Present', children=[
                html.H2("Endpoint Data"),
                dcc.Graph(
                    id='endpoint-graph1',
                    figure=px.bar(
                        df11['threat_type'].value_counts().reset_index(),
                        x=df11['threat_type'].value_counts().reset_index().index,
                        y='threat_type',
                        title='Most Common Types of Malware Detected',
                        labels={'index': 'Malware Type', 'threat_type': 'Count'},
                        color='threat_type',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    ).update_layout(
                        xaxis_title="Malware Type",
                        yaxis_title="Number of Detections",
                        showlegend=False
                    )
                ),
                html.Div([
                    html.H4("Endpoint Table"),
                    dcc.Markdown(df11.head().to_markdown())
                ]),
                html.H2("Identity Data"),
                dcc.Graph(
                    id='identity-graph1',
                    figure=px.bar(
                        df22[df22['login_status'] == 'Failure']['username'].value_counts().reset_index(),
                        x=df22[df22['login_status'] == 'Failure']['username'].value_counts().reset_index().index,
                        y='username',
                        title='Users with Most Failed Login Attempts',
                        labels={'index': 'Username', 'username': 'Failed Login Count'},
                        color='username',
                        color_discrete_sequence=px.colors.qualitative.Set1
                    ).update_layout(
                        xaxis_title="Username",
                        yaxis_title="Number of Failed Logins",
                        showlegend=False
                    )
                ),
                html.Div([
                    html.H4("Identity Table"),
                    dcc.Markdown(df22.head().to_markdown())
                ]),
                html.H2("Web Data"),
                dcc.Graph(
                    id='web-graph1',
                    figure=px.bar(
                        df44['url_accessed'].value_counts().head(10).reset_index(),
                        x=df44['url_accessed'].value_counts().head(10).reset_index().index,
                        y='url_accessed',
                        title='Top 10 Most Accessed URLs on Server',
                        labels={'index': 'URL', 'url_accessed': 'Access Count'},
                        color='url_accessed',
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    ).update_layout(
                        xaxis_title="URL",
                        yaxis_title="Number of Accesses",
                        showlegend=False
                    )
                ),
                html.Div([
                    html.H4("Web Table"),
                    dcc.Markdown(df44.head().to_markdown())
                ])
            ]),
            dcc.Tab(label='The Past', children=F1),
            dcc.Tab(label='The Future', children=[
                html.H2("Web Data"),
                dcc.Graph(
                    id='web-graph2',
                    figure=px.histogram(df4, x=df4.columns[0])  # Placeholder
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
