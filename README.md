# SI 507 Final Project

Name: Maxwell Thorpe  
Course: SI 507  
Instructor: Bobby Madamanchi  
Term: Fall 2022  

## Instructions

This project uses the Flask web framework and FlightAware's AeroAPI.  To use the Flask web framework, you will need to have a local environment that is capable of running Flask within a virtual environment.

The following instructions are from the Flask documentation:

1. Download the latest version of Python.  Flask supports versions 3.7 and up.
2. Create a virtual environment using the following commands (differs based on your OS):
    For OS:
        - $ mkdir myproject
        - $ cd myproject
        - $ python3 -m venv venv
    For Windows:
        - > mkdir myproject
        - > cd myproject
        - > py -3 -m venv venv
3. Activate the environment:
    For OS:
        - $ . venv/bin/activate
    For Windows:
        - > venv\Scripts\activate
4. Install Flask:
    - $ pip install Flask
5. Download the files from this directory and move them to your new Flask project directory.  You can start the project by either typing flask --app __init__ run or by simply running the __init__.py script.

To use the AeroAPI, you will need to register for an AeroAPI key.  Once you have obtained your key, create a file named constants.py and initialize a variable named AEROAPI_KEY.  Assign your key to this variable.  While it is not strictly necessary, you can also define and export the base API url in constants.py.

Additional Packages:
    - copy
    - json
    - requests
    - requests_cache
    - time

Additional Resources:
    - https://flask.palletsprojects.com/en/2.2.x/
    - https://flightaware.com/commercial/aeroapi/

