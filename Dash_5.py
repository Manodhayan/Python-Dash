import datetime
import pyrebase
import datetime
import time

import dash
from dash.dependencies import Input,Output,Event
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as Go
from collections import deque

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
    html.P('Ambience',style={'font-family':'Segoe UI','font-size':'30px','color':'black','margin-top':'50px','margin-left':'10px'}),
    html.Table([html.Tr([
        html.Th([html.Td([html.P('Ward:',style={'font-family':'Segoe UI','font-size':'20px','width':'80px'})]),
                 html.Td([dcc.Dropdown(
        id='node',
        value='lora_feather',options=lora_nodes,style={'display': 'inline-block','width':'200%','outline': 'none','cursor': 'pointer'},className="Ward")
            ]),
            html.Td([html.P('On Date:',style={'font-family':'Segoe UI','font-size':'20px','width':'150px','margin-left':'400px'})]),
            html.Td([dcc.DatePickerSingle(id='date-picker-single',date=datetime.date.today())])
                ])
                 ])
        ]),
    
    html.Div(children=html.Div(id='output-graph'),className='row'),
    dcc.Interval(id='delay',interval=30000)

    ],className='container',style={'width':'98%','margin-left':10,'margin-right':'20px','max-width':'50000px'})


import pandas as pd


def get_hourly_max_data(node,date):
    daily_max_data=pd.DataFrame(columns=['hour','temperature','humidity'])
    users = data.child("/"+str(date)+"/"+node).order_by_key().get()
    prev_hour=0;hourly_max_temp=0;hourly_min_temp=100;hourly_max_hum=0;hourly_min_hum=100;
    hourly_max_temp_list=[];hourly_max_hum_list=[];hourly_min_temp_list=[];hourly_min_hum_list=[]
    
    for user in users.each():
        current_hour=int(user.key()[0]+user.key()[1])
        if current_hour!=prev_hour:
            if hourly_min_temp==100:hourly_min_temp=0
            if hourly_min_hum==100:hourly_min_hum=0
            hour_data=pd.DataFrame(data=[[str(current_hour-1)+' Hour',hourly_max_temp,hourly_min_temp,hourly_max_hum,hourly_min_hum]],
                                   columns=['hour','max_temperature','min_temperature','max_humidity','min_humidity'])
            daily_max_data=daily_max_data.append(hour_data)
            hourly_temp_list=[];hourly_hum_list=[];hourly_max_temp=0;hourly_max_hum=0
            #print(current_hour)
        try:
            if(user.val()['temperature']>hourly_max_temp and current_hour==prev_hour):
                hourly_max_temp=user.val()['temperature']

            if(user.val()['temperature']<hourly_min_temp and current_hour==prev_hour):
                hourly_min_temp=user.val()['temperature']

            if(user.val()['humidity']>hourly_max_hum and current_hour==prev_hour):
                hourly_max_hum=user.val()['humidity']

            if(user.val()['humidity']<hourly_min_hum and current_hour==prev_hour):
                hourly_min_hum=user.val()['humidity']
        except:
            print("Junk Value detected")

        prev_hour=current_hour    
        #print(str(user.key())+':'+str(user.val()))
    return (daily_max_data)


@app.callback(
    Output(component_id='output-graph',component_property='children'),
    [Input(component_id='node',component_property='value'),Input(component_id='date-picker-single',component_property='date')],
    events=[Event('delay','interval')]
    )
def update_graph(input_node,date):
    graphs=[]
    last_few_x_val=[]
    last_few_temperature=[]
    last_few_humidity=[]
    required_node=input_node
    print(date)
    last_few_data = data.child("/"+str(date)+"/"+required_node).order_by_key().limit_to_last(7).get()
    hourly_data=get_hourly_max_data(required_node,date)
    for user in last_few_data.each():
        last_few_x_val.append(user.key())
        last_few_temperature.append(user.val()['temperature'])
        last_few_humidity.append(user.val()['humidity'])

   # app.config['suppress_callback_exceptions']=True
    graphs.append(
        html.Div(dcc.Graph(id='recent',
              figure={
                  'data':[
                      {'x':last_few_x_val,'y':last_few_temperature,'type':'bar','name':'Temperature'},
                      {'x':last_few_x_val,'y':last_few_humidity,'type':'bar','name':'Humidity'}
                      ],
                  'layout':Go.Layout(title='Last Updated',
                                        xaxis=dict(title='Timestamp',
                                                   titlefont=dict(
                                                    family='Courier New, monospace',
                                                    size=18,
                                                    #color='#7f7f7f'
                                                                )
                                                   ),
                                        yaxis=dict(title='Temperature & Humidity',
                                                   titlefont=dict(
                                                            family='Courier New, monospace',
                                                            size=18,
                                                            #color='#7f7f7f'
                                                            )
                                                   )
                                        )
                      
                  }
              ),className='col s12 m6 l4'
        ))
    try:
        graphs.append(
        html.Div(dcc.Graph(id='maximum',
              figure={
                  'data':[
                      {'x':hourly_data['hour'],'y':hourly_data['max_temperature'],'type':'line','name':'Temperature'},
                      {'x':hourly_data['hour'],'y':hourly_data['max_humidity'],'type':'line','name':'Humidity'}
                      ],
                  'layout':Go.Layout(title='Hourly Maximum',
                                        xaxis=dict(title='Timestamp',
                                                   titlefont=dict(
                                                    family='Courier New, monospace',
                                                    size=18,
                                                    #color='#7f7f7f'
                                                                ),
                                                   ),
                                        yaxis=dict(title='Temperature & Humidity',
                                                   titlefont=dict(
                                                            family='Courier New, monospace',
                                                            size=18,
                                                            #color='#7f7f7f'
                                                            ),range=[0,100]
                                                   )
                                        )
                      
                  }
              ),className='col s12 m6 l4'
        ))
        graphs.append(
        html.Div(dcc.Graph(id='minimum',
              figure={
                  'data':[
                      {'x':hourly_data['hour'],'y':hourly_data['min_temperature'],'type':'line','name':'Temperature'},
                      {'x':hourly_data['hour'],'y':hourly_data['min_humidity'],'type':'line','name':'Humidity'}
                      ],
                  'layout':Go.Layout(title='Hourly Minimum',
                                        xaxis=dict(title='Timestamp',
                                                   titlefont=dict(
                                                    family='Courier New, monospace',
                                                    size=18,
                                                    #color='#7f7f7f'
                                                                ),
                                                   ),
                                        yaxis=dict(title='Temperature & Humidity',
                                                   titlefont=dict(
                                                            family='Courier New, monospace',
                                                            size=18,
                                                            #color='#7f7f7f'
                                                            ),range=[0,100]
                                                   )
                                        )
                      
                  }
              ),className='col s12 m6 l4'
        ))
    except:
        print("Not Enough Data")


    return graphs

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})
if __name__ == '__main__':
    app.run_server(debug=True)

