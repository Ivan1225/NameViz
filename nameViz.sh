#!/bin/bash
echo "Building the DSL"

echo "Starting WTDSL"

if [ "$1" != "" ]; then   
    cd analysis
else
    echo "Must provied the target file"
fi