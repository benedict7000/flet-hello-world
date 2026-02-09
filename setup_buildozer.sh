#!/bin/bash
set -e

echo "Installing dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-venv git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses-dev cmake libffi-dev libssl-dev

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing Buildozer..."
pip install --upgrade pip
pip install setuptools
pip install buildozer cython==0.29.33

echo "Setup complete! Virtual environment created."
echo "To build, run: source venv/bin/activate && buildozer android debug"
