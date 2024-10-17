import os
import re
from fileinput import filename

from flask import Blueprint, request, jsonify, abort

from app.utils.support_functions import run_shell_command

api = Blueprint('api', __name__)

UPLOAD_FOLDER = 'tmp/teste-api'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

VALID_FILENAME_REGEX = re.compile(r'^[a-zA-Z0-9_-]+$')

# 1.
@api.route('/upload', methods=['PUT'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    filename = file.filename

    if not VALID_FILENAME_REGEX.match(filename):
        return jsonify({"error": "Invalid file name"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    status_code = 201 if not os.path.exists(file_path) else 204

    # Salva arquivo
    file.save(file_path)
    return jsonify({"message": "File uploaded"}), status_code

# 2.
@api.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    paginated_files = files[(page - 1) * per_page:page * per_page]
    return jsonify(paginated_files), 200

# 3.
@api.route('/user_size', methods=['GET'])
def get_user_by_size():
    filename = request.args.get('filename')
    condition = request.args.get('condition', '')

    if condition not in ['min', '']:
        return jsonify({"error": "Invalid condition"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    command = f'./utils/max-min-size.sh {file_path} {condition}'

    data, error = run_shell_command(command)

    if error:
        return jsonify({"error": error}), 500

    return jsonify(data), 200

# 4.
@api.route('/list_users', methods=['GET'])
def list_users_sorted():


    order = request.args.get('order', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    filename = request.args.get('filename')

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if order not in ['desc', '']:
        return jsonify({"error": "Invalid order"}) , 400

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404


    command = f'./utils/order-by-username.sh {file_path} {order}'

    data, error = run_shell_command(command)

    if error:
        return jsonify({"error": error}), 500

    paginated_data = data[(page - 1) * per_page:page * per_page]
    return jsonify(paginated_data), 200

# 5.
@api.route('/list_users_range', methods=['GET'])
def list_users_by_inbox_range():
    min_messages = int(request.args.get('min', 0))
    max_messages = int(request.args.get('max',))
    file_name = request.args.get('filename')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    if min_messages < 0 or max_messages < 0:
        return jsonify({"error": "Invalid range"}), 400

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    command = f'./utils/between-msgs.sh {file_path} {min_messages} {max_messages}'

    data, error = run_shell_command(command)

    if error:
        return jsonify({"error": error}), 500

    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = data[start:end]

    return jsonify(paginated_data), 200
