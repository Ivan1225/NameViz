# VISULIZATION for NameViz
This is Visulization part for NameViz project.

Our goal is to help the user find out the outlier of names in java project which violate the conventions.

Currently, we have two tabs to help the user:
* Network graph tab: In this tab, there are two graphs, one is a node-link graph and the pie chart. Which corresponded to filter used defined in the left of the tab. This tab allows the user to find out some general information about the whole project and for each file.
* Position graph tab: In this tab, there is one position graph, which shows the position of each name in a single file, it helps user quickly find out the position of outliers.

# Setup

Requirement:

* Python 3.6.5
* All packages in `requirements.txt`

# Usage

### comand

In the terminal, after open the visualization folder, then run the following command, it would start the application based one the data in `./data/output.json`.

```
bokeh serve --show app
```

## Example

### Network graph tab

### Position graph tab


