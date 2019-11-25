import json
import sys
from math import pi
import pandas as pd
import re
from bokeh.io import show, output_file
import numpy as np
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.models import Panel
from os.path import dirname, join

BASIC_TYPE = ['ClassName', 'InterfaceName', 'EnumName', 'MethodName', 'VariableName', 'ConstantName']


def generate_source(original_data):
    # empty source data
    barchart_data = {}

    for classObj in original_data:
        file_name = classObj["fileName"]
        cn_Outlier = cn_Correct = var_Outlier = var_Correct = method_Outlier = method_Correct = const_Correct = const_Outlier = 0
        subNames = classObj["subNames"]
        while len(subNames) != 0:
            for name in classObj["subNames"]:
                if name["type"] == "ClassName":
                    if name["isOutlier"]:
                        cn_Outlier = cn_Outlier + 1
                    else:
                        cn_Correct = cn_Correct + 1
                if name["type"] == "VariableName":
                    if name["isOutlier"]:
                        var_Outlier = var_Outlier + 1
                    else:
                        var_Correct = var_Correct + 1
                if name["type"] == "ConstantName":
                    if name["isOutlier"]:
                        const_Outlier = const_Outlier + 1
                    else:
                        const_Correct = const_Correct + 1
                if name["type"] == "MethodName":
                    if name["isOutlier"]:
                        error = name["errorMessage"]
                        method_Outlier = method_Outlier + 1
                    else:
                        method_Correct = method_Correct + 1
        barchart_data[file_name + "-" + "ClassName"] = [cn_Correct, cn_Outlier]
        barchart_data[file_name + "-" + "VariableName"] = [var_Correct, var_Outlier]
        barchart_data[file_name + "-" + "ConstantName"] = [const_Correct, const_Outlier]
        barchart_data[file_name + "-" + "MethodName"] = [method_Correct, method_Outlier]
    print(barchart_data)
    return barchart_data


def barChart_tab(original_data):
    # generate graph data source
    barchart_data = generate_source(original_data)

    print(barchart_data)

    # orignal test data TODO: need to use the barchart_data above
    className = ['Game', 'Flight', 'Animal']
    type = ['Class', 'Method', 'Variable', 'Constant']
    colors = ["#c9d9d3", "#718dbf", "#e84d60", "#392789"]

    arr = np.array(np.meshgrid(className, type)).T.reshape(-1, 2)
    print(arr)
    x = ','.join(str(a) for a in arr)
    factors = "[" + str(x).replace('[', '(').replace(']', ')') + "]"
    print(factors)

    # original fix test data
    # factors = [
    #     (className[0], type[0]),
    #     (className[0], type[1]),
    #     (className[0], type[2]),
    #     (className[0], type[3]),
    #     (className[1], type[0]),
    #     (className[1], type[1]),
    #     (className[1], type[2]),
    #     (className[1], type[3]),
    #     (className[2], type[0]),
    #     (className[2], type[1]),
    #     (className[2], type[2]),
    #     (className[2], type[3]),
    # ]

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

    show(p)
    tab = Panel(child=p, title='Bar Chart Graph')
    return tab
