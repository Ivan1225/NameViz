import re
import networkx as nx

from math import pi

import pandas as pd

from bokeh.models import Panel, Plot, Range1d, MultiLine, Circle, PanTool, HoverTool, BoxZoomTool, ResetTool, WheelZoomTool, ColumnDataSource
from bokeh.models.graphs import from_networkx
from bokeh.models.widgets import CheckboxGroup, Select
from bokeh.layouts import layout, row, column
from bokeh.plotting import figure
from bokeh.palettes import Category20c, Colorblind
from bokeh.transform import cumsum


# constant
BASIC_TYPE = ["class", "method", "variable", "constant"]
DETAILED_TYPE = ["class_normal", "class_outlier", "method_normal", "method_outlier", "variable_normal", "variable_outlier", "constant_normal", "constant_outlier"]

BASIC_TYPE_COLORS = {
    "class": "#155263",
    "method": "#ff6f3c",
    "variable": "#ff9a3c",
    "constant": "#ffc93c"
}
DETAILED_TYPE_COLORS = {
    "class_normal": "#2289A8",
    "class_outlier": "#155263",
    "method_normal": "#ff6f3c",
    "method_outlier": "#ff5212",
    "variable_normal": "#ff9a3c",
    "variable_outlier": "#ff8204",
    "constant_normal": "#ffc93c",
    "constant_outlier": "#ffc00e"
}

NORMAL_EDGE_COLOR, OUTLIER_EDGE_COLOR = "black", "red"

# global variable
ALL_FILES = {
    "All": ".",
}

def add_name(G, D, e, selected_type):
    name_type = e["type"]

    if name_type not in selected_type :
        return None

    name = e["name"]
    file_path = e["filePath"]
    line_number = e["lineNumber"]

    is_outlier = e["isOutlier"]
    
    var_type = e["variableType"]
    error_message = e["errorMessage"]
    
    node_name = name + "_" + file_path + "_" + str(line_number)
    type_identifier = name_type + "_outlier" if is_outlier else name_type+ "_normal"
    node_color = DETAILED_TYPE_COLORS[type_identifier]
    D[type_identifier] += 1

    G.add_node(node_name, val=name, file_path=file_path, line_number=line_number, 
        is_outlier=is_outlier, name_type=name_type, var_type=var_type, error_message=error_message, color=node_color)
    return node_name

def add_sub_names(G, D, root_node, sub_names, selected_type):
    for sub in sub_names:
        sub_node = add_name(G, D, sub, selected_type)
        if root_node is not None and sub_node is not None:
            edge_color = OUTLIER_EDGE_COLOR if G.nodes[sub_node]["is_outlier"] else NORMAL_EDGE_COLOR
            G.add_edge(root_node, sub_node, edge_color=edge_color)
        parent_node = sub_node if sub_node is not None else root_node
        add_sub_names(G, D, parent_node, sub["subNames"], selected_type)


def generate_source(original_data, selected_type, selected_file):
    # empty source data
    network_data = nx.Graph()
    pi_graph_data_o = {}
    for e in selected_type:
        pi_graph_data_o[str(e)+"_normal"] = 0
        pi_graph_data_o[str(e)+"_outlier"] = 0

    for name in original_data:
        file_path = name["filePath"]
        if file_path not in ALL_FILES.keys() :
            ALL_FILES[file_path] = file_path
        pattern = re.compile(ALL_FILES[selected_file])
        if not pattern.match(file_path) :
            continue
        node_name = add_name(network_data, pi_graph_data_o, name, selected_type)
        add_sub_names(network_data, pi_graph_data_o, node_name, name["subNames"], selected_type)

    pi_graph_data_i = pd.Series(pi_graph_data_o).reset_index(name='value').rename(columns={'index':'type'})
    pi_graph_data_i['angle'] = pi_graph_data_i['value']/pi_graph_data_i['value'].sum() * 2*pi
    pi_graph_data_i['color'] = [DETAILED_TYPE_COLORS[e] for e in pi_graph_data_o.keys()]

    pi_graph_data = ColumnDataSource(pi_graph_data_i)

    return network_data, pi_graph_data


def generate_plot(network_data, pi_graph_data):
    pi_plot = figure(plot_height=400, title="Pie Chart", toolbar_location=None,
           tools="hover", tooltips="@type: @value", x_range=(-0.5, 1.0))

    pi_plot.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='type', source=pi_graph_data)

    pi_plot.axis.axis_label=None
    pi_plot.axis.visible=False
    pi_plot.grid.grid_line_color = None

    network_plot = Plot(plot_height=700, plot_width=700,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
    network_plot.title.text = "Names Network Graph"

    node_hover_tool = HoverTool(tooltips=[("name", "@val"), ("type", "@name_type"),("outlier", "@is_outlier"),
                                            ("filePaht","@file_path"), ("lineNumber", "@line_number"),("hint", "@error_message")])
    network_plot.add_tools(node_hover_tool, PanTool(), BoxZoomTool(), WheelZoomTool(), ResetTool())

    graph_renderer = from_networkx(network_data, nx.spring_layout, scale=1, center=(0, 0))

    graph_renderer.node_renderer.glyph = Circle(size=30, fill_color="color")
    graph_renderer.edge_renderer.glyph = MultiLine(line_color="edge_color", line_alpha=0.8, line_width=1)
    network_plot.renderers.append(graph_renderer)

    return network_plot, pi_plot, graph_renderer

def network_tab(original_data):
    selected_type = BASIC_TYPE
    selected_file = "All"

    # generate graph data source
    network_data, pi_graph_data =  generate_source(original_data, selected_type, selected_file)

    # generate plot
    network_plot, pi_plot, graph_renderer = generate_plot(network_data, pi_graph_data)

    def update(attr, old, new):
        selected_type = [types_selection.labels[i] for i in types_selection.active]
        selected_file = files_selection.value
        new_network_data, new_pi_graph_data = generate_source(original_data, selected_type, selected_file)
        new_network_plot, new_pi_plot, new_graph_renderer = generate_plot(new_network_data, new_pi_graph_data)
        pi_graph_data.data.update(new_pi_graph_data.data)
        graph_renderer.node_renderer.data_source.data.update(new_graph_renderer.node_renderer.data_source.data)
        graph_renderer.edge_renderer.data_source.data.update(new_graph_renderer.edge_renderer.data_source.data)

    files_selection = Select(title="Selected file:", value="All", options=list(ALL_FILES.keys()))
    files_selection.on_change('value', update)
    types_selection = CheckboxGroup(labels=BASIC_TYPE, active = list(range(len(BASIC_TYPE))))
    types_selection.on_change('active', update)

    sliders = column(files_selection, types_selection, pi_plot)
    p_layout =  layout([[sliders, network_plot]])

    tab = Panel(child = p_layout, title = 'Network graph')
    return tab
