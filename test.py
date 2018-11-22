
import datetime
import pyrebase
import datetime
import time

import dash
from dash.dependencies import Input,Output,Event
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as Go

config = {
  "apiKey": "AIzaSyA7_XyfINo6OxLnG5mT3MP3KsKiMrCqduo",
  "authDomain": "hospital-ambience.firebaseapp.com",
  "databaseURL": "https://hospital-ambience.firebaseio.com/",
  "storageBucket": "us-central"
}

lora_nodes=[
    {'label':'Ward 1','value':'lora_feather'},
    {'label':'Ward 2','value':'lora_feather_2'},
    {'label':'Ward 3','value':'lora_feather_3'},
    {'label':'Ward 4','value':'lora_feather_4'},
    {'label':'Ward 5','value':'lora_feather_5'},
    {'label':'Ward 6','value':'lora_feature_6'}
    ]
firebase = pyrebase.initialize_app(config)
data = firebase.database()

app=dash.Dash()
app.layout=html.Div(children=[
    html.H1('Hospital Ambience Monitor'),
    dcc.Dropdown(
        id='node',
        value='lora_feather',options=lora_nodes),
    dcc.Graph(id='live_graph',animate=True),
    dcc.Interval(id='delay',interval=2000)
    ])

@app.callback(
    Output(component_id='live_graph',component_property='figure'),
    [Input(component_id='node',component_property='value')],
    events=[Event('delay','interval')]
    )
def update_graph(input_data):
    x_val=[]
    temperature=[]
    humidity=[]
    required_node=input_data
    users = data.child("/"+str(datetime.date.today())+"/"+required_node).order_by_key().limit_to_last(10).get()
    for user in users.each():
        x_val.append(datetime.datetime.strptime(user.key(), '%I:%M').time())
        temperature.append(user.val()['temperature'])
        humidity.append(user.val()['humidity'])
   # app.config['suppress_callback_exceptions']=True
    return {
                  'data':[Go.Bar(
                      x=x_val,y=temperature,name='Temperature'
                                )],
                  'layout':Go.Layout(title=input_data,
                                        xaxis=dict(title='Timestamp',
                                                   titlefont=dict(
                                                    family='Courier New, monospace',
                                                    size=18,
                                                    color='#7f7f7f'
                                                                ),
                                                   range=[min(x_val),max(x_val)]
                                                   ),
                                        yaxis=dict(title='Temperature&Humidity',
                                                   titlefont=dict(
                                                            family='Courier New, monospace',
                                                            size=18,
                                                            color='#7f7f7f'
                                                            ),
                                                   range=[0,100]
                                                   )
                                        )
                      
                  }

if __name__ == '__main__':
    app.run_server(debug=True)

