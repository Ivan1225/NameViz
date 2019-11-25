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

* [Analysis]()
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
* Jude Sidloski
* Ivan Zhang

### Visualization

* Estella Wang
* Frank Yan

