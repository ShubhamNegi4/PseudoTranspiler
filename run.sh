#!/bin/bash

# Run the first Python file
python3 main.py

# Check if the first ran successfully
if [ $? -eq 0 ]; then
    echo ""
    echo ""
    echo "file1.py executed successfully."
    echo "running python file."
    echo ""
    echo ""
    # Run the second Python file
    python3 output.py
else
    echo "main.py failed. Skipping output.py."
fi
