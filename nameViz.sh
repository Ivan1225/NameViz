#!/bin/bash
echo "Starting NamViz"

if [ "$1" != "" ]; then 
    echo "Starting Analysis"  
    cd analysis
    python3 search.py -d $1 -o ../visulization/app/data/output.json
    cd ../visulization
    echo "Starting Visualization"  
    bokeh serve --show app
else
    echo "Must provied the target project"
fi