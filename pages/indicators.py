from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv('Life.csv', sep=',')
all_countries = df['Country'].unique()

layout = dbc.Container([
    html.Div([
        html.H1("Показатели стран мира"),
        html.P(
            "Анализ основных показателей смертиности по странам мира с 2000 по 2015 годы."
            )
        ], style = {
            'backgroundColor': 'rgb(140, 130, 188)',
            'padding': '10px 5px'
        }),

    html.Div([
            html.Div([
                html.Label('Страны'),
                dcc.Dropdown(
                    id = 'crossfilter-cont',
                    options = [{'label': i, 'value': i} for i in all_countries],
                    value = ['Russian Federation'],
                    multi = True
                )
            ],
            style = {'width': '40%', 'display': 'inline-block' }),
            html.Div([
                html.Label('Основные показатели'),
                dcc.RadioItems(
                options = [
                    {'label':'Продолжительность жизни (м)', 'value': 'Life expectancy (men)'},
                    {'label':'Продолжительность жизни (ж)', 'value': 'Life expectancy(women)'},
                    {'label':'Младенческая смертность', 'value': 'Infant deaths'},
                    {'label':'Потребление алкоголя', 'value': 'Alcohol'},
                ],
                id = 'crossfilter-ind',
                value = 'Life expectancy (men)',
                labelStyle={'display': 'inline-block', 'margin': '8px'}
                )
            ],
            style = {'width': '52%',  'float': 'right', 'display': 'inline-block'})
            
        ], style = {
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),
    
    html.Div(
            dcc.Slider(
                id = 'crossfilter-year',
                min = df['Year'].min(),
                max = df['Year'].max(),
                value = 2000,
                step = None,
                marks = {str(year):
                    str(year) for year in df['Year'].unique()}
                ),
            style = {'width': '95%', 'padding': '0px 20px 20px 20px'}
        ),
    
    html.Div(
        dcc.Graph(id = 'bar'),
        style = {'width': '49%', 'display': 'inline-block'}
    ),
       
    html.Div(
        dcc.Graph(id = 'line'),
        style = {'width': '49%', 'float': 'right', 'display': 'inline-block'}
    ),

    html.Div(
        dcc.Graph(id = 'choropleth1'),
        style = {'width': '100%', 'display': 'inline-block'}
    )

], fluid= True)


@callback(
    Output('bar', 'figure'),
    [Input('crossfilter-cont', 'value'),
    Input('crossfilter-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_stacked_area(continent, indication, year):
    filtered_data = df[(df['Year'] <= year) &
        (df['Country'].isin(continent))]
    figure = px.bar(
        filtered_data,
        x = 'Year',
        y = indication,
        color = indication,
        )
    return figure

@callback(
    Output('line', 'figure'),
    [Input('crossfilter-cont', 'value'),
    Input('crossfilter-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_scatter(continent, indication, year):
    filtered_data = df[(df['Year'] <= year) &
        (df['Country'].isin(continent))]
    figure = px.line(
        filtered_data,
        x = 'Year',
        y = indication,
        color = 'Country',
        title = "Значения показателя по странам",
        markers = True,
    )
    return figure

@callback(
    Output('choropleth1', 'figure'),
    Input('crossfilter-ind', 'value')
)
def update_choropleth(indication):
    figure = px.choropleth(
        df,
        locations='Country',
        locationmode = 'country names',
        color=indication,
        hover_name='Country',
        title='Показатели по странам',
        color_continuous_scale=px.colors.sequential.BuPu,
        animation_frame='Year',
        height=650
        )
    return figure