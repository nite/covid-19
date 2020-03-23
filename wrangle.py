import numpy as np
import pycountry_convert as pc


def get_continent(country):
    try:
        country_code = pc.country_name_to_country_alpha2(country, cn_name_format='default')
        return pc.country_alpha2_to_continent_code(country_code)
    except (KeyError, TypeError):
        return country


def fix_country(country):
    if country == 'US':
        return 'United States'
    elif country == 'Korea, South':
        return 'South Korea'
    elif country == 'Taiwan*':
        return 'Taiwan*'
    return country


def wrangle_data(covid_df, pop_df):
    covid_df = covid_df.assign(Date=covid_df['Date'].astype(np.datetime64))

    covid_df['Longitude'] = covid_df['Long']
    covid_df['Latitude'] = covid_df['Lat']
    covid_df['Country'] = covid_df['Country/Region'].fillna('')
    covid_df['Country'] = covid_df['Country'].apply(fix_country)
    covid_df['Continent'] = covid_df['Country'].apply(get_continent)

    covid_df = covid_df.merge(pop_df, how='left', left_on='Country', right_on='Country')

    covid_df['State'] = covid_df['Province/State'].fillna(covid_df['Country'])
    covid_df['StateCountry'] = covid_df['State'] + ' ' + covid_df['Country']
    covid_df['Active'] = covid_df['Confirmed'] - covid_df['Recovered']

    covid_df = covid_df.assign(
        logCumConf=np.where(
            covid_df['Confirmed'] > 0,
            np.log(covid_df['Confirmed']) /
            np.where(
                covid_df['Confirmed'] > 700,
                np.log(1.01),
                np.log(1.05)
            ),
            0
        )
    )

    per_capita_adjust = 100000.0

    def per_capita(col):
        return (
                covid_df[col]
                / covid_df['Population']
                * per_capita_adjust
        ).round(0)

    covid_df['ActivePerCapita'] = per_capita('Active')
    covid_df['ConfirmedPerCapita'] = per_capita('Confirmed')
    covid_df['RecoveredPerCapita'] = per_capita('Recovered')
    covid_df['DeathsPerCapita'] = per_capita('Deaths')

    covid_df['log10'] = np.where(covid_df['Confirmed'] > 0,
                                 np.ceil(np.log10(covid_df['Confirmed'])), 0)
    covid_df['log_group'] = np.power(10, covid_df['log10'] - 1).astype(np.int).astype(str) \
                            + '-' + np.power(10, covid_df['log10']).astype(np.int).astype(str)
    covid_df['Description'] = covid_df['State'] + ', ' \
                              + covid_df['Country'] + ', ' \
                              + covid_df['Continent'] + '<br>' \
                              + 'Confirmed: ' + covid_df['Confirmed'].astype(str) + '<br>' \
                              + 'Confirmed Per Capita: ' + covid_df['ConfirmedPerCapita'].astype(str) + '<br>' \
                              + 'Recovered: ' + covid_df['Recovered'].astype(str) + '<br>' \
                              + 'Active: ' + covid_df['Active'].astype(str) + '<br>' \
                              + 'Deaths: ' + covid_df['Deaths'].astype(str) + '<br>' \
                              + 'Confirmed Range: ' + covid_df['log_group'].astype(str) + '<br>'
    return covid_df
