import networkx as nx

from bokeh.models import Panel, Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool
from bokeh.models.graphs import from_networkx
from bokeh.models.widgets import CheckboxGroup
from bokeh.layouts import row
from bokeh.palettes import Spectral4

# function to build network graph tab

TYEP = ["class", "method", "variable", "constant"]

NORMAL_EDGE_COLOR, OUTLIER_EDGE_COLOR = "black", "red"

def add_node(G, e, selections):
    name_type = e["type"]

    if name_type not in selections :
        return None

    name = e["name"]
    file_path = e["filePath"]
    line_number = e["lineNumber"]

    isOutlier = e["isOutlier"]
    
    var_type = e["variableType"]
    error_message = e["errorMessage"]
    
    node_name = name + "_" + file_path + "_" + str(line_number)
    G.add_node(node_name, val=name, file_path=file_path, line_number=line_number, 
        isOutlier=isOutlier, name_type=name_type, var_type=var_type, error_message=error_message)
    return node_name

def add_subNames(G, root_node, subNames, selections):
    for sub in subNames:
        sub_node = add_node(G, sub, selections)
        if root_node is not None and sub_node is not None:
            edge_color = OUTLIER_EDGE_COLOR if G.nodes[sub_node]["isOutlier"] else NORMAL_EDGE_COLOR
            G.add_edge(root_node, sub_node, edge_color=edge_color)
        parent_node = sub_node if sub_node is not None else root_node
        add_subNames(G, parent_node, sub["subNames"], selections)
        

def build_graph(data, selections):
    G = nx.Graph()
    for e in data:
        node_name = add_node(G, e, selections)
        add_subNames(G, node_name, e["subNames"], selections)

    return G


def get_plot(G):
    plot = Plot(plot_width=400, plot_height=400,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
    plot.title.text = "Names Network Graph"

    node_hover_tool = HoverTool(tooltips=[("name", "@val"), ("type", "@name_type")])
    plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

    graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))

    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    graph_renderer.edge_renderer.glyph = MultiLine(line_color="edge_color", line_alpha=0.8, line_width=1)
    plot.renderers.append(graph_renderer)

    return plot, graph_renderer


def network_tab(data):

    initail_selections = TYEP

    # build G
    G = build_graph(data, initail_selections)

    plot, graph_renderer = get_plot(G)

    def update(attr, old, new):
        curr_selections = [types_selection.labels[i] for i in types_selection.active]
        new_G = build_graph(data, curr_selections)
        n_plot, n_graph_renderer = get_plot(new_G)
        graph_renderer.node_renderer.data_source.data.update(n_graph_renderer.node_renderer.data_source.data)
        graph_renderer.edge_renderer.data_source.data.update(n_graph_renderer.edge_renderer.data_source.data)

    types_selection = CheckboxGroup(labels=TYEP, active = list(range(len(TYEP))))
    types_selection.on_change('active', update)

    layout = row(types_selection, plot)

    tab = Panel(child = layout, title = 'Network graph')
    return tab
