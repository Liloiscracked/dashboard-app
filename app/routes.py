from flask import render_template, request, redirect, url_for, session, flash
from two_g_data import DataProcessor_2g
from run import app, get_db_connection
from werkzeug.security import check_password_hash

@app.route("/", methods=["GET"])
def index():
    if "user" in session:
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        session['user'] = email
        flash('Login successful!')
        return redirect(url_for("home"))
    else:
        flash('Invalid email or password.')
        return redirect(url_for("index"))

@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        file1 = request.files.get("file1")
        file2 = request.files.get("file2")

        if file1 and file2:
            data_processor = DataProcessor_2g(file1, file2)
            return render_template('index.html',
                                   map_html1=data_processor.map_html1,
                                   throughput_html1=data_processor.throughput_html1,
                                   rsrp_html1=data_processor.rsrp_html1,
                                   map_html2=data_processor.map_html2,
                                   throughput_html2=data_processor.throughput_html2,
                                   rsrp_html2=data_processor.rsrp_html2)
    return render_template("upload.html")

@app.route("/2g", methods=["POST", "GET"])
def two_g():
    if request.method == 'POST':
        file1 = request.files.get('file1')
        file2 = request.files.get('file2')

        if file1 and file2:
            data_processor = DataProcessor_2g(file1, file2)

            return render_template('2g.html',
                                   polqa_html1=data_processor.polqa_html1,
                                   polqa_html2=data_processor.polqa_html2,
                                   map_html1=data_processor.map_html1,
                                   map_html2=data_processor.map_html2,
                                   rx_qual_html1=data_processor.rx_qual_html1,
                                   rx_qual_html2=data_processor.rx_qual_html2,
                                   rx_qual_map_html1=data_processor.rx_qual_map_html1,
                                   rx_qual_map_html2=data_processor.rx_qual_map_html2,
                                   gsm_power_html1=data_processor.gsm_power_html1,
                                   gsm_power_html2=data_processor.gsm_power_html2,
                                   gsm_power_map_html1=data_processor.gsm_power_map_html1,
                                   gsm_power_map_html2=data_processor.gsm_power_map_html2,
                                   polqa_stats1=data_processor.polqa_stats1,
                                   polqa_stats2=data_processor.polqa_stats2,
                                   rx_qual_stats1=data_processor.rx_qual_stats1,
                                   rx_qual_stats2=data_processor.rx_qual_stats2,
                                   gsm_power_stats1=data_processor.gsm_power_stats1,
                                   gsm_power_stats2=data_processor.gsm_power_stats2)

    return render_template('2g.html', polqa_html1='', polqa_html2='', map_html1='', map_html2='',
                           rx_qual_html1='', rx_qual_html2='', rx_qual_map_html1='', rx_qual_map_html2='',
                           gsm_power_html1='', gsm_power_html2='', gsm_power_map_html1='', gsm_power_map_html2='',
                           polqa_stats1={}, polqa_stats2={}, rx_qual_stats1={}, rx_qual_stats2={},
                           gsm_power_stats1={}, gsm_power_stats2={})
