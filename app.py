from flask import Flask, render_template, request, send_file, jsonify, session
from card_generator import generate_card_route  # 関数をimport
import os,uuid
os.chdir(os.path.dirname(__file__)) 
app = Flask(__name__)

app.secret_key = os.urandom(24)  # セッション管理用

BASE_TEMP_DIR = "temp_images"

@app.before_request
def ensure_user_session():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())

def get_user_temp_dir():
    user_dir = os.path.join(BASE_TEMP_DIR, session["user_id"])
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/card_generated")
def card_page():
    return render_template("card_generated.html")

# 追加
@app.route("/generate_card", methods=["POST"])
def generate_card():
    user_dir = get_user_temp_dir()
    return generate_card_route()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Renderが割り当てるポートを取得
    app.run(host="0.0.0.0", port=port)

