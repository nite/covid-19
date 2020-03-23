# Coronavirus COVID-19 Dashboard - Global Kaggle Data

#### Live Dashboard
https://covid19-dash.herokuapp.com/  

#### Data Source
https://www.kaggle.com/imdevskp/corona-virus-report

#### Dev notes 

To get up & running, create a venv, activate & run: 
```bash
pip install -r requirements.txt
python app.py
# in another terminal, activate again & run:
pip install jupyterlab
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install jupyterlab-plotly
jupyter labextension install plotlywidget
jupyter lab build
jupyter lab # and open notebooks/
```

To recompile sass: `sudo npm i -g sass` and either add it to your IDE, or run: `sass assets/styles.scss`

#### Features/notes:

* Kaggle Data Source: https://www.kaggle.com/imdevskp/corona-virus-report
* Click play on map to animate over time - bubble size is log, hover for data.
* Hover over barplot to filter timeseries by country - bar size is log10.
* python Plotly Dash app (an open source dataviz library)

#### Potential Future Developments 
* Daily auto-updates
* correlating other data (economic factors, comparison with flu data etc)
* better granularity/grouping/drill-down, brushing/linking & crossfiltering 
* machine learning predictions, 

#### Screencast 

![screencast](https://covid19-dash.herokuapp.com/assets/covid-dash-screencast.gif "Screencast")

https://covid19-dash.herokuapp.com/assets/covid-dash-screencast.mp4
