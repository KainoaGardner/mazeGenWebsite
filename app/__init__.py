from flask import Flask

app = Flask(__name__)
app.secret_key = "maze"


from app import routes
