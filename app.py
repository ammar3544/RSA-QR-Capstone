from flask import Flask, request, render_template, send_from_directory, redirect, url_for, flash, jsonify
import os, struct, base64, datetime, re, hashlib, time
from werkzeug.utils import secure_filename
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps
from werkzeug.datastructures import FileStorage
from livereload import Server
import qrcode

# ------------------- Flask Setup -------------------
app = Flask(__name__, static_folder='image', template_folder='webpage')
app.secret_key = os.environ.get('FLASK_SECRET', 'supersecret')
app.config["TEMPLATES_AUTO_RELOAD"] = True   # <— agar HTML langsung update
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0  # <— cegah cache browser

# ------------------- User Management -------------------
USERS = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'client': {'password': 'client123', 'role': 'client'},
    'mitra': {'password': 'mitra123', 'role': 'mitra'},
}

class User(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.role = role
    def get_role(self):
        return self.role

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        return User(user_id, USERS[user_id]['role'])
    return None

def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.get_role() != role:
                return 'Unauthorized', 403
            return f(*args, **kwargs)
        return wrapped
    return decorator

# ------------------- Routes -------------------
@app.route("/")
def home():
    path = "webpage/home.html"
    if os.path.exists(path):
        print("Last modified home.html:", time.ctime(os.path.getmtime(path)))
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = USERS.get(username)
        if user_data and user_data['password'] == password:
            user = User(username, user_data['role'])
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.')
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():
    os.makedirs('keys', exist_ok=True)
    pub_keys = [f for f in os.listdir('keys') if f.startswith('public_')]
    priv_keys = [f for f in os.listdir('keys') if f.startswith('private_')]
    return render_template('index.html', pub_keys=pub_keys, priv_keys=priv_keys, is_logged_in=current_user.is_authenticated)

@app.route("/generate-keys", methods=["POST"])
@login_required
def route_generate_keys():
    bits = int(request.form.get("bits", 2048))
    key = RSA.generate(bits)
    priv_key = key.export_key()
    pub_key = key.publickey().export_key()

    os.makedirs("keys", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    priv_path = os.path.join("keys", f"private_{timestamp}.pem")
    pub_path = os.path.join("keys", f"public_{timestamp}.pem")

    with open(priv_path, "wb") as f:
        f.write(priv_key)
    with open(pub_path, "wb") as f:
        f.write(pub_key)

    flash(f"RSA keys generated: {os.path.basename(pub_path)} & {os.path.basename(priv_path)}")
    return redirect(url_for("index"))

# ------------------- Key Detection / Verification -------------------
def extract_public_key_from_bytes(bts: bytes):
    try:
        text = bts.decode('utf-8', errors='ignore')
    except Exception:
        return None
    m = re.search(r'(-----BEGIN PUBLIC KEY-----.+?-----END PUBLIC KEY-----)', text, re.S)
    return m.group(1).encode('utf-8') if m else None

def pubkey_fingerprint_sha256(pem_bytes: bytes):
    return hashlib.sha256(pem_bytes).hexdigest()

def load_server_pubkeys(folder='keys'):
    pubkeys = {}
    if not os.path.exists(folder):
        return pubkeys
    for fn in os.listdir(folder):
        if fn.startswith('public_'):
            try:
                path = os.path.join(folder, fn)
                with open(path, 'rb') as f:
                    pem = f.read()
                fp = pubkey_fingerprint_sha256(pem)
                pubkeys[fp] = {'filename': fn, 'pem': pem}
            except Exception:
                continue
    return pubkeys

def verify_signature_with_pubkey(file_bytes, signature_bytes, pubkey_pem):
    try:
        key = RSA.import_key(pubkey_pem)
        h = SHA256.new(file_bytes)
        try:
            signature_bytes = base64.b64decode(signature_bytes, validate=True)
        except Exception:
            pass
        pkcs1_15.new(key).verify(h, signature_bytes)
        return True
    except Exception:
        return False

@app.route('/verify-upload', methods=['GET', 'POST'])
@login_required
def verify_upload():
    if request.method == 'GET':
        return render_template('verify.html')

    uploaded = request.files.get('file')
    sig_file = request.files.get('signature')
    pubkey_file = request.files.get('public_key')

    if not uploaded:
        flash('Tidak ada file yang diunggah.')
        return redirect(url_for('index'))

    file_bytes = uploaded.read()
    embedded_pub_pem = extract_public_key_from_bytes(file_bytes)
    uploaded_pub_pem = pubkey_file.read() if pubkey_file else None
    signature_bytes = sig_file.read() if sig_file else None

    server_pubkeys = load_server_pubkeys('keys')

    results = {
        'filename': uploaded.filename,
        'embedded_pubkey_found': bool(embedded_pub_pem),
        'signature_provided': bool(signature_bytes),
        'notes': []
    }

    if embedded_pub_pem:
        fp = pubkey_fingerprint_sha256(embedded_pub_pem)
        match = fp in server_pubkeys
        results['notes'].append(f"Fingerprint embedded: {fp} | Match server: {match}")

    if uploaded_pub_pem:
        fp2 = pubkey_fingerprint_sha256(uploaded_pub_pem)
        match2 = fp2 in server_pubkeys
        results['notes'].append(f"Fingerprint uploaded: {fp2} | Match server: {match2}")

    if signature_bytes:
        if embedded_pub_pem:
            ok = verify_signature_with_pubkey(file_bytes, signature_bytes, embedded_pub_pem)
            results['notes'].append(f"Signature valid (embedded key): {ok}")
        if uploaded_pub_pem:
            ok2 = verify_signature_with_pubkey(file_bytes, signature_bytes, uploaded_pub_pem)
            results['notes'].append(f"Signature valid (uploaded key): {ok2}")
    else:
        results['notes'].append("Tidak ada signature diunggah — verifikasi terbatas.")

    return render_template('verify_result.html', results=results)

# ------------------- Role-based Pages -------------------
@app.route('/admin')
@login_required
@role_required('admin')
def admin_dashboard():
    return render_template('admin.html')

@app.route('/client')
@login_required
@role_required('client')
def client_dashboard():
    return render_template('client.html')

@app.route('/mitra')
@login_required
@role_required('mitra')
def mitra_dashboard():
    return render_template('mitra.html')

# ------------------- Run Server -------------------
if __name__ == '__main__':
    print("Server Flask sedang dijalankan... buka http://127.0.0.1:5000 di browser.")
    server = Server(app.wsgi_app)
    server.watch('webpage/*.*')
    server.serve(port=5000, host='0.0.0.0', debug=True)
