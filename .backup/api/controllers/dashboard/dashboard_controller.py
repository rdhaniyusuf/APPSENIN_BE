from flask import Blueprint, request, jsonify

dashboard_controller = Blueprint('dashboard_controller', __name__)

@dashboard_controller.route('/all_absense', methods=['GET'])
def parse_data():
    try:
        data = request.get_json()
        # Add your parsing logic here
        parsed_data = {}  # Replace with actual parsing result
        return jsonify(parsed_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400