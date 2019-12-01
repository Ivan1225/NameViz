# NameViz

This is the project to help the user analysis the name in java project for variables, class and so on, and provide a visualization to find out the outlier which violates the naming conventions.

## Desgin

### [First Design doc](https://docs.google.com/document/d/1hWxpEQqI-LhiZdUcbBOHfuQPMWn3_As5hJdQ9lsX3_Y/edit)

Goal:
* help programmers evaluate the consistency of their naming conventions according to their type: class name, function name, and variable name. Programmers can find outliers, which are names that do not match the convention for their type.


Data structure:
```json
[
  {
    "fileName": ,
    "filePath": ,
    "isOutlier": ,
    "errorMessage": ,
    "line": ,
    "name": ,
    "parent": ,
    "position": ,
    "subNames": [],
    "type": ,
    "variableType": 
  },

]
```

Visualization:
* summary table


### Second desgin

In second iteration of desgin after prototype user study, we mainly improve our visualization, we add more ways to help the user easily find out the oulier.

Visualization:
* node-link graph ![pic](./resources/node.jpg)
* pie chart ![pic](./resources/pie.jpg)
* scatter plot ![pic](./resources/scatter.jpg)
* bar chart ![pic](./resources/bar.jpg)

## Detail

* [Analysis](./analysis/README.md)
* [Visualization](./visulization/README.md)

# Setup

Requirement:

* Python 3.7.5
* All packages in `requirements.txt`

## Usage

### script

we provide a smiple script to run our tool, which would do analysis first and then visualize in web page.

## command

```
./nameViz.sh [file path to target project folder]
```

## Demo

![demo](./resources/demo.gif)


## Work

This part shows each member response to which part of project.

### Analysis

* David Chen
  * Write regex and algorithm that search different kinds of names from java file
* Jude Sidloski
  * Wrote the part of the program that traverses a project directory.
  * Track nesting of code to determine what classes and methods names belong to.
  * Designed data structure for a name object and the tree that holds all the names.
* Ivan Zhang
  * Research resource of accuracy of WordNet words bank.
  * Using regex and WordNet to lexically analysis each word in a name to check if the word match correct pattern of Java naming convention.
  * Test with different name and name type combinations.
  * Combine outlier result to output.

### Visualization

* Estella Wang
   * Explored the usage of Bokeh and Pandas library to facilate our visualization
   * Mainly worked on implementation of bar chart
   * Added hover effects and filter for user interaction
   
* Frank Yan
  * Build outer frame for visualization
  * Mainly worked on implementation of node graph, pie chart and scatter plot.
  * Add simple filiter allow users to foucus on part of project thery want to do visualization.

