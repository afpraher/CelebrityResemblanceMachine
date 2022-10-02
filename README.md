# CelebrityResemblanceMachine

An AI designed to recognise your celebrity lookalike.

## Automatic Setup

Note:   
CMake and the Visual Studio Build Tools will still have to be installed manually

* Open the projects folder
* Execute the `install.ps1` script
* Open the command line
* Run `python crm.py`

## Manual Setup

* Extract the `Celebs.zip` file
* Open the command line
* Navigate to the projects folder
* Install the necessary requirements
* Run the program using `python crm.py`

For help run `python crm.py --help`

## Requirements

Libraries:
* argparse
* matplotlib
* numpy
* opencv-python
* pillow
* face_recognition

You will also need CMake.
Get it from [cmake.org](https://cmake.org/download/)

As well as the Visual Studio Build Tools.
Make sure to install the workload "Desktop Development with C++"   
You can find the installer here [visualstudio.microsoft.com](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)