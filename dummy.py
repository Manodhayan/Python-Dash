import dash
from dash.dependencies import Input,Output
import dash_core_components as dcc
import dash_html_components as html
import datetime
lora_nodes=[
    {'label':'Ward 1','value':'lora_feather'},
    {'label':'Ward 2','value':'lora_feather_2'},
    {'label':'Ward 3','value':'lora_feather_3'},
    {'label':'Ward 4','value':'lora_feather_4'},
    {'label':'Ward 5','value':'lora_feather_5'},
    {'label':'Ward 6','value':'lora_feature_6'}
    ]

app=dash.Dash()
app.layout=html.Div(children=[
    html.Div(children=[
        html.P('Ambiencee',style={'font-family':'Segoe UI','font-size':'30px','color':'black','margin-top':'50px','margin-left':'10px'},)
        
        ],style={'background-color':'White'}),
    html.Table([html.Tr([
        html.Th([html.Td([html.P('Ward:',style={'font-family':'Segoe UI','font-size':'20px',})]),html.Td([html.P("Ward:")
            ])
                 ])
        ])
                       ])
    #html.Th(dcc.Dropdown(
    #    id='node',
    #    value='lora_feather',options=lora_nodes,style={'display': 'inline-block','width':'40%','outline': 'none','cursor': 'pointer'},className="Ward")),
    #html.Th(dcc.DatePickerSingle(id='date-picker-single',date=datetime.date.today()))))
    ])
def update_value(input_data):
    return("Input:{}".format(input_data))


if __name__ == '__main__':
    app.run_server(debug=True)