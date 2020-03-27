import os

import numpy as np
import plotly.graph_objects as go
from plotly import express as px

plot_config = {
    'modeBarButtonsToRemove': [
        'lasso2d',
        'hoverClosestCartesian',
        'hoverCompareCartesian',
        'toImage',
        'sendDataToCloud',
        'hoverClosestGl2d',
        'hoverClosestPie',
        'toggleHover',
        'resetViews',
        'toggleSpikelines',
        'resetViewMapbox'
    ]
}

plot_palette = [
    '#185d6a',
    '#385e4c',
    '#597043',
    '#7a8339',
    '#9b9530',
    '#bca727',
    '#ddb91e',
    '#ffcc14',
]

mapbox_token = os.environ.get('MAPBOX_TOKEN', '')

mapbox_cofig = dict(
    accesstoken=mapbox_token,
    style='mapbox://styles/nite/ck7z7pu6p1utj1jlkfgpwvo3q', )

bggolor = '#24252A'
default_layout = {
    'margin': {'r': 5, 't': 20, 'l': 5, 'b': 30},
    'paper_bgcolor': bggolor,
    'plot_bgcolor': bggolor,
}

plot_threshold = 35

empty_plot = px.line(template='plotly_dark', )


def get_default_color(count_col='Confirmed'):
    if count_col == 'Confirmed':
        return '#6195d2'
    if count_col == 'Active':
        return '#2B34B9'
    if count_col == 'Recovered':
        return '#BC472A'


def get_map_plot(covid_df, count_col='Confirmed'):
    df = covid_df[covid_df[count_col] > 0]

    # todo: convert to https://plot.ly/python/mapbox-county-choropleth/
    values = df['logCumConf' if count_col == 'Confirmed' else count_col]

    # map_fig = px.scatter_geo(lat=map_df['Latitude'],
    #                          lon=map_df['Longitude'],
    #                          hover_name=map_df['Description'],
    #                          size=map_df['logCumConf'],
    #                          animation_frame=map_df['Date'],
    #                          projection='natural earth',
    #                          template='plotly_dark')

    fig = px.scatter_mapbox(
        mapbox_style='carto-darkmatter',
        lat=df['Latitude'],
        lon=df['Longitude'],
        hover_name=df['Description'],
        size=values,
        opacity=0.6,
        size_max=50,
        zoom=.95,
        animation_frame=df['Date'].astype(str),
        center=go.layout.mapbox.Center(
            lat=14,
            lon=21
        ),
        template='plotly_dark',
        color_discrete_sequence=[get_default_color(count_col)],
    )

    if mapbox_token:
        fig.update_layout(
            mapbox=mapbox_cofig
        )

    fig.update_layout(
        **default_layout,
    )
    # map_fig.update_geos(fitbounds='locations')
    fig.update_traces(
        marker=go.scattermapbox.Marker(
            color='rgb(255, 0, 0)',
            opacity=0.7,
            sizeref=.5,
        ),
        selector=dict(geo='geo')
    )
    return fig


def get_total_timeseries(covid_df, country=None, per_capita=False):
    title = country if country else 'All Countries'
    covid_df = covid_df.assign(Date=covid_df['Date'].astype(np.datetime64))
    suffix = 'PerCapita' if per_capita else ''
    df = covid_df[covid_df['Confirmed'] > 0] \
        .groupby(['Date']).sum() \
        .reset_index() \
        .melt(id_vars='Date',
              value_vars=[
                  'Confirmed' + suffix,
                  'Recovered' + suffix,
                  'Active' + suffix,
                  'Deaths' + suffix
              ]) \
        .sort_values('Date')
    fig = px.line(
        df,
        x='Date',
        y='value',
        labels={
            'Date': 'Date',
            'value': 'Count',
        },
        color='variable',
        line_shape='spline',
        render_mode='svg',
        title=title,
        template='plotly_dark',
        color_discrete_sequence=plot_palette,
    )
    fig.update_layout(
        hovermode='x',
        legend_title='',
        title={
            'text': title,
            'y': 0.97,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
        },
        **default_layout,
    )
    return fig


def get_country_timeseries(covid_df, count_col='Confirmed'):
    last_df = covid_df[covid_df['Date'] == covid_df['Date'].max()]

    top_countries = last_df \
        .nlargest(plot_threshold, count_col) \
        .reset_index()['Country'].unique()

    df = covid_df[covid_df['Country'].isin(top_countries)] \
        .groupby(['Date', 'Country']) \
        .sum().reset_index() \
        .sort_values(['Date', 'Country'])

    fig = px.line(
        x=df['Date'],
        y=df[count_col],
        color=df['Country'],
        labels={
            'y': count_col,
            'x': 'Date',
        },
        hover_name=df['Country'],
        line_shape='spline',
        render_mode='svg',
        template='plotly_dark',
        color_discrete_sequence=plot_palette,
    )
    fig.update_layout(
        hovermode='x',
        legend_title='',
        **default_layout,
    )
    return fig


def get_bar_plot(covid_df, count_col='Confirmed'):
    last_df = covid_df[covid_df['Date'] == covid_df['Date'].max()]
    df = last_df.groupby([
        'Country',
    ]) \
        .sum().reset_index() \
        .nlargest(plot_threshold, count_col) \
        .sort_values(count_col)

    if count_col == 'Confirmed':
        values = np.log10(df[count_col])
        x_label = count_col + ' (log10)'
    else:
        values = df[count_col]
        x_label = count_col

    fig = px.bar(
        y=df['Country'],
        x=values,
        text=df[count_col],
        # color=df['Continent'],
        orientation='h',
        hover_name=count_col + ': ' + df[count_col].astype(str),
        labels={
            'x': x_label,
            'y': ''
        },
        template='plotly_dark',
        color_discrete_sequence=[get_default_color(count_col)],
    )
    fig.update_layout(
        selectdirection='v',
        **default_layout,
    )
    return fig
