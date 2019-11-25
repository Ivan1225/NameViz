from bokeh.models import Panel, Plot, Circle, HoverTool, ColumnDataSource, LinearAxis
from bokeh.models.widgets import CheckboxGroup, Select
from bokeh.layouts import layout, column
from bokeh.plotting import figure
from bokeh.palettes import Set1


# constant
BASIC_TYPE = ['ClassName', 'InterfaceName', 'EnumName', 'MethodName', 'VariableName', 'ConstantName']

BASIC_TYPE_COLORS = {}
COLORS = Set1[len(BASIC_TYPE)+1]

for i in range(len(BASIC_TYPE)):
    BASIC_TYPE_COLORS[BASIC_TYPE[i]] = COLORS[i+1]

BASIC_TYPE_COLORS["Outlier"] = COLORS[0]

NORMAL_EDGE_COLOR, OUTLIER_EDGE_COLOR = "black", "red"

# global variable
ALL_FILES = []
XY_RANGES = {}

def add_name(data, e, selected_type):
    name_type = e["type"]
    name = e["name"]

    if name_type in selected_type and name is not None:
        data["line"].append(e["line"])
        data["position"].append(e["position"])
        data["name"].append(name)
        data["type"].append(name_type)
        data["isOutlier"].append(e["isOutlier"])
        data["hint"].append(e["errorMessage"])
        type_identifier = "Outlier" if e["isOutlier"] else name_type
        node_color = BASIC_TYPE_COLORS[type_identifier]
        data["color"].append(node_color)
    
    for sub in e["subNames"]:
        add_name(data, sub, selected_type)

def generate_source(original_data, selected_type, selected_file):
    data = {"line": [], "position": [], "name": [] , "type": [], "isOutlier": [], "hint": [], "color": []}

    for name in original_data:
        file_path = name["filePath"]
        if not file_path == selected_file :
            continue
        add_name(data, name, selected_type)
    
    return  ColumnDataSource(data)

def generate_plot(source, selected_file):
    plot = figure()
    plot.title.text = "Position plot"
    
    plot.axis.visible=False
    xaxis = LinearAxis()
    xaxis.axis_label = "position"
    plot.add_layout(xaxis, 'above')
    yaxis = LinearAxis()
    yaxis.axis_label = "line"
    plot.add_layout(yaxis, 'left')
    plot.x_range.start = 0
    plot.y_range.start = XY_RANGES[selected_file][1]
    plot.x_range.end = XY_RANGES[selected_file][0]
    plot.y_range.end = 0
    
    plot.circle(x='position', y='line',color='color', size=10, source=source)

    plot.y_range.flipped = True

    node_hover_tool = HoverTool(tooltips=[("name", "@name"), ("type", "@type"),("outlier", "@isOutlier"),
                                            ("lineNumber", "@line"), ("position", "@position"), ("hint", "@hint")])
    plot.add_tools(node_hover_tool)

    return plot

def position_tab(original_data):
    selected_type = BASIC_TYPE

    for e in original_data :
        fp = e["filePath"]
        if fp not in ALL_FILES:
            ALL_FILES.append(fp)
            s = generate_source(original_data, selected_type, fp)
            XY_RANGES[fp] = [max(s.data["position"]) + 5, max(s.data["line"]) + 5]
    
    selected_file = ALL_FILES[0]

    source =  generate_source(original_data, selected_type, selected_file)

    scatter_plot = generate_plot(source, selected_file)

    def update(attr, old, new):
        selected_type = [types_selection.labels[i] for i in types_selection.active]
        selected_file = files_selection.value
        new_scatter_plot = generate_plot(generate_source(original_data, selected_type, selected_file), selected_file)
        p_layout.children[0].children[1] = new_scatter_plot

    files_selection = Select(title="Selected file:", value=selected_file, options=ALL_FILES)
    files_selection.on_change('value', update)
    types_selection = CheckboxGroup(labels=BASIC_TYPE, active = list(range(len(BASIC_TYPE))))
    types_selection.on_change('active', update)

    sliders = column(files_selection, types_selection)
    p_layout =  layout([[sliders, scatter_plot]])

    tab = Panel(child = p_layout, title = 'Position graph')
    return tab