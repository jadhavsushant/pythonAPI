# pythonAPI
Power up building python API with Flask

## Python virtual environment 

    python3 -m venv <venv-name>
    
    .\venv\Scripts\activate
    # ...
    deactivate


## Docker build Images
    
    # Build the image
    docker build -t flask-sm-rest-api .
    
    # Create docker container so start using it for python development
    docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-sm-rest-api