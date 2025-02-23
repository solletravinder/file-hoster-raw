import os
import boto3
from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from config import config
from auth import auth, token_required
from middleware import limiter, csrf
from models import db, bcrypt, User, File
import sqlitecloud

app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(auth, url_prefix="/auth")
limiter.init_app(app)
csrf.init_app(app)


# Set Database URL (SQLite or SQLiteCloud)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")


app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'zip', 'mp4', 'avi', 'mkv', 'mov'}

s3_client = boto3.client(
    "s3",
    endpoint_url=config.ENDPOINT_URL,
    aws_access_key_id=config.ACCESS_KEY,
    aws_secret_access_key=config.SECRET_KEY_DO,
    verify=False
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_size_limit(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0, 0)
    
    if file.filename.endswith('.zip'):
        return size <= 2 * 1024 * 1024 * 1024  # 2GB limit for ZIP files
    else:
        return size <= 1 * 1024 * 1024 * 1024  # 1GB limit for all other files

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/keep-db-alive", methods=["GET"])
def keep_db_alive():
    try:
        # Attempt to execute a simple query to check the database connection
        db.session.execute('SELECT 1')
        return jsonify({"status": "success", "message": "Database connection is alive"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



@app.route("/delete-file/<int:file_id>", methods=["DELETE"])
@token_required
def delete_file(current_user, file_id):
    file = File.query.filter_by(id=file_id, user_id=current_user.id).first()
    
    if not file:
        return jsonify({"error": "File not found or unauthorized"}), 404

    # Delete from DigitalOcean Spaces
    try:
        s3_client.delete_object(Bucket=config.SPACE_NAME, Key=file.filename)
    except Exception as e:
        return jsonify({"error": "Failed to delete file from storage", "details": str(e)}), 500

    # Remove from database
    db.session.delete(file)
    db.session.commit()

    return jsonify({"message": "File deleted successfully"}), 200


@app.route("/my-files", methods=["GET"])
@token_required
def my_files(current_user):
    user_files = File.query.filter_by(user_id=current_user.id).all()
    
    files_list = [{
        "id": file.id,
        "filename": file.filename,
        "url": file.file_url,
        "uploaded_at": file.uploaded_at
    } for file in user_files]

    return jsonify({"files": files_list}), 200


@app.route("/upload", methods=["POST"])
@token_required
def upload_file(current_user):
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Invalid file"}), 400

    filename = secure_filename(file.filename)

    # Save locally (temporary)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Upload to DigitalOcean Spaces
    try:
        s3_client.upload_file(file_path, config.SPACE_NAME, filename, ExtraArgs={"ACL": "public-read"})
        file_url = f"{config.ENDPOINT_URL}/{config.SPACE_NAME}/{filename}"
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

    # Save file metadata to the database
    new_file = File(filename=filename, file_url=file_url, user_id=current_user.id)
    db.session.add(new_file)
    db.session.commit()

    return jsonify({"message": "File uploaded", "url": file_url})


@app.route('/uploads/<filename>')
@token_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
