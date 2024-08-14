import pandas as pd
from flask import render_template, request, redirect, url_for, session, flash
from two_g_data import DataProcessor_2g
from run import app, get_db_connection
from werkzeug.security import check_password_hash
from four_g_data import DataProcessor_4g
from five_g_data import DataProcessor_5g
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


@app.route('/4g', methods=['GET', 'POST'])
def four_g():
    if request.method == 'POST':
        # Get uploaded files
        file1 = request.files.get('file1')
        file2 = request.files.get('file2')

        if not file1 or not file2:
            return "Both files are required!", 400

        # Create DataProcessor_4g instances for each file
        processor1 = DataProcessor_4g(file1)
        processor2 = DataProcessor_4g(file2)

        # Generate visualizations for File 1
        rsrp_html1 = processor1.rsrp_html
        cinr_html1 = processor1.cinr_html
        rsrq_html1 = processor1.rsrq_html
        polqa_html1 = processor1.polqa_html
        rsrp_map_html1 = processor1.rsrp_map_html
        cinr_map_html1 = processor1.cinr_map_html
        rsrq_map_html1 = processor1.rsrq_map_html
        polqa_map_html1 = processor1.polqa_map_html
        earfcn_pie_html1 = processor1.earfcn_pie_html
        earfcn_map_html1 = processor1.earfcn_map_html

        # Generate visualizations for File 2
        rsrp_html2 = processor2.rsrp_html
        cinr_html2 = processor2.cinr_html
        rsrq_html2 = processor2.rsrq_html
        polqa_html2 = processor2.polqa_html
        rsrp_map_html2 = processor2.rsrp_map_html
        cinr_map_html2 = processor2.cinr_map_html
        rsrq_map_html2 = processor2.rsrq_map_html
        polqa_map_html2 = processor2.polqa_map_html
        earfcn_pie_html2 = processor2.earfcn_pie_html
        earfcn_map_html2 = processor2.earfcn_map_html

        return render_template('4g.html',
                               rsrp_html1=rsrp_html1,
                               rsrp_stats1=processor1.stats('Serving RS Info-Serving RSRP (d Bm)'),
                               cinr_html1=cinr_html1,
                               rsrq_html1=rsrq_html1,
                               polqa_html1=polqa_html1,
                               rsrp_map_html1=rsrp_map_html1,
                               cinr_map_html1=cinr_map_html1,
                               rsrq_map_html1=rsrq_map_html1,
                               polqa_map_html1=polqa_map_html1,
                               earfcn_pie_html1=earfcn_pie_html1,
                               earfcn_map_html1=earfcn_map_html1,
                               rsrp_html2=rsrp_html2,
                               rsrp_stats2=processor2.stats('Serving RS Info-Serving RSRP (d Bm)'),
                               cinr_html2=cinr_html2,
                               rsrq_html2=rsrq_html2,
                               polqa_html2=polqa_html2,
                               rsrp_map_html2=rsrp_map_html2,
                               cinr_map_html2=cinr_map_html2,
                               rsrq_map_html2=rsrq_map_html2,
                               polqa_map_html2=polqa_map_html2,
                               earfcn_pie_html2=earfcn_pie_html2,
                               earfcn_map_html2=earfcn_map_html2)
    return render_template('4g.html',rsrp_stats1 ={},rsrp_stats2 = {})


@app.route('/5g', methods=['GET', 'POST'])
def five_g():
    if request.method == 'POST':
        # Get uploaded files
        file1 = request.files.get('file1')
        file2 = request.files.get('file2')

        if not file1 or not file2:
            return "Both files are required!", 400

        # Create DataProcessor_4g instances for each file
        processor1 = DataProcessor_5g(file1)
        processor2 = DataProcessor_5g(file2)

        # Generate visualizations for File 1
        rsrp_html1 = processor1.rsrp_html
        cinr_html1 = processor1.cinr_html
        dl_html1 = processor1.dl_html
        rsrp_map_html1 = processor1.rsrp_map_html
        cinr_map_html1 = processor1.cinr_map_html
        dl_map_html1 = processor1.dl_map_html

        # Generate visualizations for File 2
        rsrp_html2 = processor2.rsrp_html
        cinr_html2 = processor2.cinr_html
        dl_html2 = processor2.dl_html
        rsrp_map_html2 = processor2.rsrp_map_html
        cinr_map_html2 = processor2.cinr_map_html
        dl_map_html2 = processor2.dl_map_html

        return render_template('5g.html',
                               rsrp_html1=rsrp_html1,
                               rsrp_stats1=processor1.stats('Serving RS Info-Serving RSRP (d Bm)'),
                               cinr_html1=cinr_html1,
                               cinr_stats1=processor1.stats('Serving RS Info-NR Best SS-SINR'),
                               dl_html1=dl_html1,
                               dl_stats1=processor1.stats('Data Throughput-NR PDCP downlink throughput (Mbps)'),
                               rsrp_map_html1=rsrp_map_html1,
                               cinr_map_html1=cinr_map_html1,
                               dl_map_html1=dl_map_html1,
                               rsrp_html2=rsrp_html2,
                               rsrp_stats2=processor2.stats('Serving RS Info-Serving RSRP (d Bm)'),
                               cinr_html2=cinr_html2,
                               cinr_stats2=processor2.stats('Serving RS Info-NR Best SS-SINR'),
                               dl_html2=dl_html2,
                               dl_map_html2= dl_map_html2,
                               dl_stats2=processor2.stats('Data Throughput-NR PDCP downlink throughput (Mbps)'),
                               rsrp_map_html2=rsrp_map_html2,
                               cinr_map_html2=cinr_map_html2,
                               rsrq_map_html2=dl_map_html2,)
    return render_template('5g.html',rsrp_stats1 ={},rsrp_stats2 = {}, cinr_stats1 = {}, cinr_stats2 = {},dl_stats1 = {},dl_stats2 = {},)

