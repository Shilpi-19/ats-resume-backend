# from flask import Flask
# from flask_cors import CORS
# from routes.user_routes import user_bp
# import dotenv
# from dotenv import load_dotenv
# import os
# import cohere

# # Load environment variables from .env file
# load_dotenv()

# co = cohere.Client(os.getenv("COHERE_API_KEY"))

# app = Flask(__name__)
# CORS(app)

# # Register your routes
# from routes.application_routes import application_bp
# from routes.user_routes import user_bp

# app.register_blueprint(application_bp)
# app.register_blueprint(user_bp, url_prefix="/users")

# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask
from flask_cors import CORS
from routes.user_routes import user_bp
from services.db_service import client  # Import client to confirm connection
import dotenv
from dotenv import load_dotenv
import os
import cohere
 
# Load environment variables from .env file
load_dotenv()
 
co = cohere.Client(os.getenv("COHERE_API_KEY"))
 
app = Flask(__name__)
CORS(app)
 
# Debugging: Check MongoDB connection
try:
    client.admin.command('ping')
    print("MongoDB connection verified in app.py.")
except Exception as e:
    print(f"MongoDB connection error in app.py: {e}")
 
# Register your routes
from routes.application_routes import application_bp
from routes.user_routes import user_bp
from routes.all_application_routes import get_application_bp
 
app.register_blueprint(application_bp)
app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(get_application_bp) 
if __name__ == "__main__":
    app.run(debug=True)