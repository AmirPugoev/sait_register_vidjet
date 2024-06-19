#
from flask import Flask
from config import Config
import routes 

app = Flask(__name__)
app.config.from_object(Config)

routes.create_routes(app)
if __name__ == '__main__':
    app.run(debug=True)
