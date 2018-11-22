
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
    html.Div([html.P("Ward:"),
    dcc.Dropdown(
        id='node',
        value='lora_feather',options=lora_nodes,style={'display': 'inline-block','width':'40%'},className="Ward"),
    dcc.DatePickerSingle(id='date-picker-single',date=datetime.date.today())],style={'marginBottom': 50, 'marginTop': 25}),
    html.Div(id='output-graph'),
    dcc.Interval(id='delay',interval=30000)
    ])

@app.callback(
    Output(component_id='output-graph',component_property='children'),
    [Input(component_id='node',component_property='value'),Input(component_id='date-picker-single',component_property='date')],
    events=[Event('delay','interval')]
    )
def update_graph(input_node,date):
    x_val=[]
    temperature=[]
    humidity=[]
    required_node=input_node
    print(date)
    users = data.child("/"+str(date)+"/"+required_node).order_by_key().limit_to_last(10).get()
    for user in users.each():
        x_val.append(user.key())
        temperature.append(user.val()['temperature'])
        humidity.append(user.val()['humidity'])
   # app.config['suppress_callback_exceptions']=True

    return dcc.Graph(id='example',
              figure={
                  'data':[
                      {'x':x_val,'y':temperature,'type':'bar','name':'Temperature'},
                      {'x':x_val,'y':humidity,'type':'bar','name':'Humidity'}
                      ],
                  'layout':Go.Layout(title=input_node,
                                        xaxis=dict(title='Timestamp',
                                                   titlefont=dict(
                                                    family='Courier New, monospace',
                                                    size=18,
                                                    color='#7f7f7f'
                                                                )
                                                   ),
                                        yaxis=dict(title='Temperature&Humidity',
                                                   titlefont=dict(
                                                            family='Courier New, monospace',
                                                            size=18,
                                                            color='#7f7f7f'
                                                            )
                                                   )
                                        )
                      
                  },
              )

if __name__ == '__main__':
    app.run_server(debug=True)

