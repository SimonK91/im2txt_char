#!/usr/bin/env bash
PYTHON=python2.7
PIP=pip

# Setup python environment
if [[ $(ls -1 ${PYTHON}_env | wc -l) -eq 0 ]]; then
    # Create fresh
    echo "Creating new virtual environment for $PYTHON"
    virtualenv --python=$(which $PYTHON) ${PYTHON}_env

fi
# Activate
echo "Activating python environment"
. ${PYTHON}_env/bin/activate

# Install dependencies
echo "Installing python dependencies"
$PIP install --upgrade pip
$PIP install keras_applications
$PIP install keras_preprocessing
$PIP install tensorflow_estimator
$PIP install wheel
$PIP install matplotlib
$PIP install pandas
$PIP install numpy
$PIP install tensorflow


PYTHON=$(which $PYTHON)
