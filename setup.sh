 #!/bin/bash

# Update package lists
apt-get update

# Install missing OpenCV dependencies
apt-get install -y libgl1-mesa-glx

# Install Python dependencies
pip install -r requirements.txt
