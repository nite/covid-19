# Data Source https://www.kaggle.com/imdevskp/corona-virus-report

import logging
import os

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State

from plots import plot_config, get_map_plot, get_total_timeseries, get_country_timeseries, get_bar_plot
from wrangle import wrangle_data

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
locks = {}

template = 'plotly_dark'
default_layout = {
    'autosize': True,
    'xaxis': {'title': None},
    'yaxis': {'title': None},
    'margin': {'l': 40, 'r': 20, 't': 40, 'b': 10},
    'paper_bgcolor': '#303030',
    'plot_bgcolor': '#303030',
    'hovermode': 'x',
}

external_stylesheets = [
    'https://codepen.io/mikesmith1611/pen/QOKgpG.css',
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.1/css/all.min.css',
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
)

app.index_string = open('index.html', 'r').read()

try:
    import kaggle

    kaggle.api.authenticate()
    kaggle.api.dataset_download_files('imdevskp/corona-virus-report', path='./data', unzip=True)
except:
    print('download kaggle auth to ~/.kaggle.json')

covid_df = pd.read_csv('./data/covid_19_clean_complete.csv')
pop_df = pd.read_csv('./data/macro_corona_data.csv')
covid_df = wrangle_data(covid_df, pop_df)


def get_graph(class_name, **kwargs):
    return html.Div(
        className=class_name + ' plotz-container',
        children=[
            dcc.Graph(**kwargs),
            html.I(className='fa fa-expand'),
        ],
    )


def dropdown_options(col):
    return [{'label': name, 'value': name} for name in col]


screen1 = html.Div(
    className='parent',
    children=[
        get_graph(
            class_name='div1',
            figure=get_map_plot(covid_df),
            id='map_graph',
            config=plot_config,
        ),
        get_graph(
            class_name='div2',
            figure=get_bar_plot(covid_df),
            id='bar_graph',
            config=plot_config,
            clear_on_unhover=True,
        ),
        get_graph(
            class_name='div3',
            figure=get_country_timeseries(covid_df),
            id='country_graph',
            config=plot_config,
        ),
        get_graph(
            class_name='div4',
            figure=get_total_timeseries(covid_df),
            id='total_graph',
            config=plot_config,
        ),
    ])

countries = covid_df['Country'].unique()
countries.sort()

# dcc.Dropdown(
# options=dropdown_options(countries),

control_panel = html.Div(
    className='header',
    children=[
        dcc.RadioItems(
            id='count_category',
            className='radio-group',
            options=dropdown_options(['Confirmed', 'Active', 'Recovered']),
            value='Confirmed',
            labelStyle={'display': 'inline-block'}
        ),
        html.Span('|'),
        dcc.RadioItems(
            id='count_type',
            className='radio-group',
            options=[
                {'label': 'Per Capita', 'value': 'per_capita'},
                {'label': 'Actual', 'value': 'actual'}
            ],
            value='actual',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Input(
            id='country_input',
            type='text',
            debounce=True,
        ),
    ])

about_app = html.Div(
    children=[
        html.Ul([
            html.Li(
                html.A('Global Kaggle Data',
                       href='https://www.kaggle.com/imdevskp/corona-virus-report')),
            html.Li(
                html.A('Open Source', href='https://github.com/nite/covid-19')),
        ]),
        html.P('''
        This interactive data visualisation dashboard illustrates what is possible using 
        the Open Source & free python Plotly Dash library and very little code
        to deliver some simple & powerful insights into the global data of the 
        Covid-19 Coronavirus. 
        This is rapid app development: not intended for 'production', more for prototyping.
        Think of it as a completely free Tableau, with the power of python for data science
        & machine learning directly accessible. The source code is in the GitHub link above.
        '''),
        html.P('''
        The dashboard is optimised for desktop or laptop - it may work on tablet, however is clunky on mobile.
        '''),
        html.P('''
        All plots are interactive - hit play on the map, hover over bubbles, lines & points 
        for tooltips (dynamic annotations), zoom using your mouse (drag to select area to 
        zoom into), mouse wheel or trackpad, and double click to zoom out & reset. 
        Click lines in legends to hide & show, or double-click to show only 
        one line. Be sure to use zoom on the map, the bubbles overlap & become a lot clearer 
        on zooming.
        '''),
        html.P('''
        To maximise any plot to fill the window, use the expand icon in top left. 
        '''),
        html.P('''
        To filter the bottom middle timeline to a country, hover over a horizontal bar
        in the rightmost plot.
        '''),
        html.P('''
        To switch between Confirmed, Active & Recorded, and Per Capita/Actual,
         use the radio buttons in the control panel, top right.
        '''),
        html.P('''
        The code is entirely Open Source, and is intended as a showcase of what is possible 
        in very few lines of python Plotly Dash code. 
        For example, take a look at plot.py in the github repo for the single line of 
        Plotly Express code to generate the scatter_mapbox with animating timeline.  
        '''),
        html.P('''
        We use Global Kaggle Data which is generated & cleaned from the CSSEGISandData/COVID-19 
        dataset (also on GitHub).
        '''),
        html.P('''
        Per Capita numbers are number / Population * 100,000 
        '''),
        html.P('''
        It was rapid to develop, and trivial to host (for free) via Heroku - see the GitHub link for details. 
        '''),
        html.P('''
        There is an accompanying Jupter Notebook in the Open Source GitHub Repo (above) 
        '''),
    ]
)

modal = html.Div(
    [
        dbc.Button('About the Dashboard',
                   id='open_modal',
                   color='link'),
        dbc.Modal(
            [
                dbc.ModalHeader('COVID-19 Open Source Dashboard | Global John Hopkins Data'),
                dbc.ModalBody(
                    children=[
                        about_app,
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button('Close',
                               id='close',
                               color='link',
                               className='ml-auto')
                ),
            ],
            id='modal',
        ),
    ]
)

app.layout = html.Div(
    className='covid-container',
    children=[
        html.Div(
            className='header',
            children=[
                html.Div(
                    className='title',
                    children=[
                        html.H4('COVID-19 Dashboard | Global Kaggle Data'),
                    ]
                ),
                html.Div(
                    className='header',
                    children=[
                        modal,
                        control_panel
                    ])
            ]),
        screen1
    ])


@app.callback(
    Output('modal', 'is_open'),
    [Input('open_modal', 'n_clicks'), Input('close', 'n_clicks')],
    [State('modal', 'is_open')],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output('country_input', 'value'),
    [
        Input('bar_graph', 'hoverData'),
    ])
def update_x_timeseries(hoverData):
    logger.debug(hoverData)
    return hoverData['points'][0]['y'] if hoverData else ''


@app.callback(
    Output('map_graph', 'figure'),
    [
        Input('count_type', 'value'),
        Input('count_category', 'value'),
    ])
def update_map_plot(count_type, count_category):
    count_col = count_category if count_type == 'actual' else count_category + 'PerCapita'
    return get_map_plot(covid_df, count_col)


@app.callback(
    Output('bar_graph', 'figure'),
    [
        Input('count_type', 'value'),
        Input('count_category', 'value'),
    ])
def update_bar_plot(count_type, count_category):
    count_col = count_category if count_type == 'actual' else count_category + 'PerCapita'
    return get_bar_plot(covid_df, count_col)


@app.callback(
    Output('country_graph', 'figure'),
    [
        Input('count_type', 'value'),
        Input('count_category', 'value'),
    ])
def update_bar_plot(count_type, count_category):
    count_col = count_category if count_type == 'actual' else count_category + 'PerCapita'
    return get_country_timeseries(covid_df, count_col)


@app.callback(
    Output('total_graph', 'figure'),
    [
        Input('country_input', 'value'),
        Input('count_type', 'value')
    ])
def update_x_timeseries(country, count_type):
    df = covid_df[covid_df['Country'] == country] \
        if country \
        else covid_df
    return get_total_timeseries(
        df,
        country=country,
        per_capita=count_type == 'per_capita')


if __name__ == '__main__':
    logger.info('app running')
    port = os.environ.get('PORT', 9000)
    debug = bool(os.environ.get('PYCHARM_HOSTED', os.environ.get('DEBUG', False)))
    app.run_server(debug=debug,
                   host='0.0.0.0',
                   port=port)
