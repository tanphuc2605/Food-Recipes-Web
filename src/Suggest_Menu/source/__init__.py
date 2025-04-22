from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for frontend access
    
    # Register routes
    from source.routes import recipes
    app.register_blueprint(recipes.bp)
    
    return app