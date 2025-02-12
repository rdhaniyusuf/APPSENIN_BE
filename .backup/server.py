from flask import Flask, request
from flask_cors import CORS
from api.routes.user_route import user_bp

from utils.connect_db import connect_db

connection = connect_db()
app = Flask(__name__)
# Aktifkan CORS untuk semua request
CORS(app, supports_credentials=True)

# Pastikan semua route memiliki prefix "/api"
app.register_blueprint(user_bp, url_prefix="/api/")

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(f'Page not found: {request.url}')
    return "Page not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
