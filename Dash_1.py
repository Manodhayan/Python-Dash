import dash
from dash.dependencies import Input,Output
import dash_core_components as dcc
import dash_html_components as html

app=dash.Dash()
app.layout=html.Div(children=[
    html.H1('Dash tutorials'),
    dcc.Graph(id='example',
              figure={
                  'data':[
                      {'x':[1,2,3,4,5],'y':[2,6,8,2,1],'type':'line','name':'boats'},
                      {'x':[1,2,3,4,5],'y':[2,6,8,12,1],'type':'bar','name':'cars'}
                      ],
                  'layout':{
                      'title':'A Dash Example'
                      }
                  }
              )
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
