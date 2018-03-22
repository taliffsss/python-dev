import dash
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader.data import DataReader
import time
from collections import deque
import plotly.graph_objs as go
import random
import requests

app = dash.Dash('vehicle-data')

main = "https://www.msw.ph/"
mswmega = "https://megasportsworld.com"
mswlive = "https://mswlive.com/"
mswsites = "https://www.mswsites.com/"
facebook = "https://www.facebook.com/"
google = "https://www.google.com/"

msw = requests.post(main)
mega = requests.post(mswmega)
live = requests.post(mswlive)
sites = requests.post(mswsites)
fb = requests.post(facebook)
g = requests.post(google)

mswmain = msw.elapsed.total_seconds()
mswmega = mega.elapsed.total_seconds()
mswlive = live.elapsed.total_seconds()
mswsites = sites.elapsed.total_seconds()
face = fb.elapsed.total_seconds()
gm = g.elapsed.total_seconds()

max_length = 50
times = deque(maxlen=max_length)
mswlivesites = deque(maxlen=max_length)
mainsites = deque(maxlen=max_length)
mswmedia = deque(maxlen=max_length)
portalsites = deque(maxlen=max_length)
fbsites = deque(maxlen=max_length)
googlecom = deque(maxlen=max_length)

data_dict = {"Main Sites":mainsites,
"Mega Sports World":mswmedia,
"MSW Sites":portalsites,
"MSW LIVE":mswlivesites,
"Facebook":fbsites,
"Google":googlecom}


def update_obd_values(times, mswlivesites, mainsites, mswmedia, portalsites, fbsites, googlecom):

    times.append(time.time())
    if len(times) == 1:
        #starting relevant values
        mswlivesites.append(random.uniform(mswlive,mswlive))
        mainsites.append(random.uniform(mswmain,mswmain))
        mswmedia.append(random.uniform(mswmega,mswmega))
        portalsites.append(random.uniform(mswsites,mswsites))
        fbsites.append(random.uniform(face,face))
        googlecom.append(random.uniform(gm,gm))
    else:
        for data_of_interest in [mswlivesites, mainsites, mswmedia, portalsites, fbsites, googlecom]:
            data_of_interest.append(data_of_interest[-1]+data_of_interest[-1]*random.uniform(-0.0001,0.0001))

    return times, mswlivesites, mainsites, mswmedia, portalsites, fbsites, googlecom

times, mswlivesites, mainsites, mswmedia, portalsites, fbsites, googlecom = update_obd_values(times, mswlivesites, mainsites, mswmedia, portalsites, fbsites, googlecom)

app.layout = html.Div([
    html.Div([
        html.H4('Real time Domain Statistic Graph',
                style={'float': 'left',
                       }),
        ]),
    dcc.Dropdown(id='vehicle-data-name',
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=['Facebook','Google'],
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=100),
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})


@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('vehicle-data-name', 'value')],
    events=[dash.dependencies.Event('graph-update', 'interval')]
    )
def update_graph(data_names):
    graphs = []
    update_obd_values(times, mswlivesites, mainsites, mswmedia, portalsites, fbsites, googlecom)
    if len(data_names)>2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'


    for data_name in data_names:

        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb"
            )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
                                                        yaxis=dict(range=[min(data_dict[data_name]),max(data_dict[data_name])]),
                                                        margin={'l':50,'r':1,'t':45,'b':1},
                                                        title='{}'.format(data_name))}
            ), className=class_choice))

    return graphs


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})