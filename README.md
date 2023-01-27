Setup virtualenv:

`python -m venv env`

And activate it:

`source env/bin/activate`

Install requirements with pip:

`pip install -r requirements.txt`

Run server with:

`python -m uvicorn main:app --reload`
