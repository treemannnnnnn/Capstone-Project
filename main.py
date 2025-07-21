import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
from datetime import datetime

def main():
    # Load datasets
    df1 = pd.read_csv('Endpoint.csv')
    df2 = pd.read_csv('Identity.csv')
    df3 = pd.read_csv('Network.csv')
    df4 = pd.read_excel('Web.xlsx')
    df5 = pd.read_csv('Incidents.csv')

    # Filter recent entries for "The Present"
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

    # The Past - Heatmap
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
        title='Malware Detections by Date and Hour'
    )
    heatmap_fig.update_layout(height=600)

    # The Past - Threat Types by Severity
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

    # The Future - Time-to-Resolution Analysis
    response_data = df5[df5['resolution_status'] == 'Resolved'].copy()
    avg_response_time = response_data.groupby('category')['response_time_minutes'].mean().reset_index()
    avg_response_time = avg_response_time.sort_values('response_time_minutes', ascending=False)

    response_fig = px.bar(
        avg_response_time,
        x='category',
        y='response_time_minutes',
        title='Average Incident Response Time by Category',
        labels={'category': 'Threat Category', 'response_time_minutes': 'Avg Response Time (minutes)'},
        color='response_time_minutes',
        color_continuous_scale='Blues'
    )
    response_fig.update_layout(
        xaxis_title='Threat Category',
        yaxis_title='Average Response Time (minutes)'
    )

    # The Future - Malware Detection Trend Projection
    df1['detection_time'] = pd.to_datetime(df1['detection_time'])
    df1['date_only'] = pd.to_datetime(df1['detection_time'].dt.date)  

    trend_data = df1.groupby('date_only').size().reset_index(name='count')

    trend_fig = px.scatter(
        trend_data,
        x='date_only',
        y='count',
        trendline='ols',
        title='Malware Detections Over Time with Trendline',
        labels={'date_only': 'Date', 'count': 'Malware Detections'},
        color_discrete_sequence=['#636EFA']
    )
    trend_fig.update_traces(mode='lines+markers')
    trend_fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Number of Malware Detections',
        height=600
    )

    F3 = html.Div([
        html.H2("Time-to-Resolution Analysis"),
        dcc.Graph(figure=response_fig),
        html.H2("Malware Detection Trend Projection"),
        dcc.Graph(figure=trend_fig)
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
                )
            ]),
            dcc.Tab(label='The Past', children=F1),
            dcc.Tab(label='The Future', children=F3),
        ])
    ])

    app.run(debug=True)

if __name__ == "__main__":
    main()
