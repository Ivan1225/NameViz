import json
from math import pi
import pandas as pd

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.models import Panel


BASIC_TYPE = ['ClassName', 'InterfaceName', 'EnumName', 'MethodName', 'VariableName', 'ConstantName']

BASIC_TYPE_COLORS = {}
COLORS = Set1[len(BASIC_TYPE)+1]

for i in range(len(BASIC_TYPE)):
    BASIC_TYPE_COLORS[BASIC_TYPE[i]] = COLORS[i+1]

def barChart_tab(data):
    # with open('Test Data/package.json') as f:
    #     testData = json.load(f)
    #
    # correctNum = outlier = 0
    #
    # for data in testData:
    #     print('isOutlier: ' + str(o['isOutlier']))
    #     if data['fileName']:
    #         correctNum = correctNum + 1
    #     else:
    #         outlier = outlier + 1

    className = ['Game', 'Flight', 'Animal']
    type = ['Class', 'Method', 'Variable', 'Constant']
    colors = ["#c9d9d3", "#718dbf", "#e84d60", "#392789"]

    factors = [
        (className[0], type[0]), (className[0], type[1]), (className[0], type[2]), (className[0], type[3]),
        (className[1], type[0]), (className[1], type[1]), (className[1], type[2]), (className[1], type[3]),
        (className[2], type[0]), (className[2], type[1]), (className[2], type[2]), (className[2], type[3]),
    ]

    result = ['correctNaming', 'outlier']

    source = ColumnDataSource(data=dict(
        x=factors,
        correctNaming=[5, 5, 6, 5, 5, 4, 5, 6, 7, 8, 6, 9],
        outlier=[5, 7, 9, 4, 5, 4, 7, 7, 7, 6, 6, 7],
    ))

    p = figure(x_range=FactorRange(*factors), plot_height=250,
               toolbar_location=None, tools="")

    p.vbar_stack(result, x='x', width=0.9, alpha=0.5, color=["blue", "red"], source=source,
                 legend_label=result)

    p.y_range.start = 0
    p.y_range.end = 18
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_center"
    p.legend.orientation = "horizontal"

    tab = Panel(child=p, title='Bar Chart Graph')
    return tab
