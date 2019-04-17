import os
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html

from apps import basicApp

from graphdb_connector import connector


driver = connector.getGraphDatabaseConnectionConfiguration()

DataTypes = ['proteomics', 'clinical', 'wes', 'longitudinal_proteomics', 'longitudinal_clinical']
Users = [(u['name']) for u in driver.nodes.match("User")]
Tissues = [(t['name']) for t in driver.nodes.match("Tissue")]
Diseases = [(d['name']) for d in driver.nodes.match("Disease")]
#ClinicalVariables = [(c['name']) for c in driver.nodes.match("Clinical_variable")]
ClinicalVariables = pd.read_csv('./apps/templates/tmp_data/clinicalvariables.csv')

template_cols = pd.read_excel(os.path.join(os.getcwd(), 'apps/templates/ClinicalData_template.xlsx'))
template_cols = template_cols.columns.tolist()


class ProjectCreationApp(basicApp.BasicApp):
    def __init__(self, title, subtitle, description, layout = [], logo = None, footer = None):
        self.pageType = "projectCreationPage"
        basicApp.BasicApp.__init__(self, title, subtitle, description, self.pageType, layout, logo, footer)
        self.buildPage()

    def buildPage(self):
        self.add_basic_layout()
        layout = [html.Div([
                    html.Div([html.Div(children=[html.A(children=html.Button('Download Template (.xlsx)', id='download_button', style={'maxWidth':'130px'}), id='download_link', style={'marginLeft': '90%'})]),
                              html.H4('Project information', style={'marginTop':0}),
                              html.Div(children=[html.Label('Project name:', style={'marginTop':10}),
                                                 dcc.Input(id='project name', placeholder='Insert name...', type='text', style={'width':'100%', 'height':'35px'})],
                                                 style={'width':'100%'}),
                              html.Div(children=[html.Label('Project Acronym:', style={'marginTop':10}),
                                                 dcc.Input(id='project acronym', placeholder='Insert name...', type='text', style={'width':'100%', 'height':'35px'})],
                                                 style={'width':'100%'}),
                              html.Div(children=[html.Label('Project Responsible:', style={'marginTop':10})],
                                                 style={'width':'49%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(children=[html.Label('Project Data Types:', style={'marginTop':10})],
                                                 style={'width':'49%', 'marginLeft':'2%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(id='dumm-div', style={'display':'none'}),
                              html.Div(children=[dcc.Dropdown(id='responsible-picker', options=[{'label':i, 'value':i} for i in Users], value=['',''], multi=True, style={'width':'100%'})],                                    
                                                 style={'width':'20%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(children=[html.Button('Add', id='add_responsible', style={'height':'35px'})],
                                                 style={'width':'10%', 'marginLeft': '0.4%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(children=[dcc.Dropdown(id='data-types-picker', options=[{'label':i, 'value':i} for i in DataTypes], value=['',''], multi=True, style={'width':'100%'})],
                                                 style={'width':'20%', 'marginLeft': '20.6%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(children=[html.Button('Add', id='add_datatype', style={'height':'35px'})],
                                                 style={'width':'10%', 'marginLeft': '0.4%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(children=[dcc.Input(id='responsible', value='', type='text', style={'width':'100%', 'height':'35px', 'marginTop':5})],
                                                 style={'width':'49%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(children=[dcc.Input(id='data-types', value='', type='text', style={'width':'100%', 'height':'35px', 'marginTop':5})],
                                                 style={'width':'49%', 'marginLeft':'2%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(children=[html.Label('Project Participants:', style={'marginTop':10})],
                                                 style={'width':'49%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(children=[html.Label('Project Tissue:', style={'marginTop':10})],
                                                 style={'width':'49%', 'marginLeft':'2%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(children=[dcc.Dropdown(id='participant-picker', options=[{'label':i, 'value':i} for i in Users], value=['',''], multi=True, style={'width':'100%'})],                                    
                                                 style={'width':'20%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(children=[html.Button('Add', id='add_participant', style={'height':'35px'})],
                                                 style={'width':'10%', 'marginLeft': '0.4%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(children=[dcc.Dropdown(id='tissue-picker', options=[{'label':i, 'value':i} for i in Tissues], value=['',''], multi=True, style={'width':'100%'})],
                                                 style={'width':'20%', 'marginLeft': '20.6%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(children=[html.Button('Add', id='add_tissue', style={'height':'35px'})],
                                                 style={'width':'10%', 'marginLeft': '0.4%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(children=[dcc.Input(id='participant', value='', type='text', style={'width':'100%', 'height':'35px', 'marginTop':5})],
                                                 style={'width':'49%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(children=[dcc.Input(id='tissue', value='', type='text', style={'width':'100%', 'height':'35px', 'marginTop':5})],
                                                 style={'width':'49%', 'marginLeft':'2%', 'verticalAlign':'top', 'display':'inline-block'}),
                              html.Div(children=[html.Label('Project Description:', style={'marginTop':10}),
                                                 dcc.Textarea(id='project description', placeholder='Enter description...', style={'width':'100%'})]),
                              html.Div(children=[html.Label('Starting Date:', style={'marginTop':10}),
                                                 dcc.DatePickerSingle(id='date-picker-start', placeholder='Select date...', clearable=True)],
                                                 style={'width':'30%', 'verticalAlign':'top', 'marginTop':10, 'display':'inline-block'}),
                              html.Div(children=[html.Label('Ending Date:', style={'marginTop':10}),
                                                 dcc.DatePickerSingle(id='date-picker-end', placeholder='Select date...', clearable=True)],
                                                 style={'width':'30%', 'verticalAlign':'top', 'marginTop':10, 'display':'inline-block'}),
                              html.Div(children=[html.Button('Create Project', id='project_button')],
                                                 style={'fontSize':'22px', 'marginLeft':'87.3%'}),
                              html.Div(id='project-creation', style={'fontSize':'20px', 'marginLeft':'70%'})]),
                    html.Hr()])]

        self.extend_layout(layout)