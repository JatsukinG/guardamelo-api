# Guardamelo Django API


## How to install the project in localhost
1. Clone the repo
2. `cd` into the `guardamelo-api` folder
3. Create a virtual environment and active it
4. `pip install -r requirements.txt`
5. `CORS_ALLOWED_ORIGINS="http://localhost:5174" python manage.py runserver`

**Note:** Is important run command with `CORS_ALLOWED_ORIGINS` variable to allow queries from localhost, en futuras versiones cuando se use docker no habra necesidad.