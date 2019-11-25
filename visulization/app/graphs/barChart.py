from bokeh.models import Panel, Plot, Circle, HoverTool, ColumnDataSource, LinearAxis
from bokeh.models.widgets import CheckboxGroup, Select
from bokeh.layouts import layout, column
from bokeh.plotting import figure

BASIC_TYPE = ['ClassName', 'InterfaceName', 'EnumName', 'MethodName', 'VariableName', 'ConstantName']
ALL_FILES = []

COLORS = ["#c9d9d3", "#718dbf"]
TYPE = ["normal", "outlier"]


def add_name(data, e, selected_type):
    name_type = e["type"]
    name = e["name"]

    if name_type in selected_type and name is not None:
        index = selected_type.index(name_type)
        if e["isOutlier"]:
            data["outlier"][index] += 1
        else:
            data["normal"][index] += 1

    for sub in e["subNames"]:
        add_name(data, sub, selected_type)


def generate_source(original_data, selected_type, selected_file):
    data = {"type": selected_type, "normal": [0] * len(selected_type), "outlier": [0] * len(selected_type)}

    for name in original_data:
        file_path = name["filePath"]
        if not file_path == selected_file:
            continue
        add_name(data, name, selected_type)

    print(data)

    return data


def generate_plot(data, selected_type):
    p = figure(x_range=selected_type, plot_height=350, title="Outlier count by type",
               toolbar_location=None, tools="hover", tooltips="$name @type: @$name")

    p.vbar_stack(TYPE, x='type', width=0.9, source=data, color=COLORS, legend_label=TYPE)

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    return p


def bar_tab(original_data):
    selected_type = BASIC_TYPE

    for e in original_data:
        fp = e["filePath"]
        if fp not in ALL_FILES:
            ALL_FILES.append(fp)

    selected_file = ALL_FILES[0]

    source = generate_source(original_data, selected_type, selected_file)

    bar_plot = generate_plot(source, selected_type)

    def update(attr, old, new):
        selected_type = [types_selection.labels[i] for i in types_selection.active]
        selected_file = files_selection.value
        new_bar_plot = generate_plot(generate_source(original_data, selected_type, selected_file), selected_type)
        p_layout.children[0].children[1] = new_bar_plot

    types_selection = CheckboxGroup(labels=BASIC_TYPE, active=list(range(len(BASIC_TYPE))))
    types_selection.on_change('active', update)
    files_selection = Select(title="Selected file:", value=selected_file, options=ALL_FILES)
    files_selection.on_change('value', update)

    sliders = column(files_selection, types_selection)
    p_layout = layout([[sliders, bar_plot]])

    tab = Panel(child=p_layout, title='Bar chart')
    return tab