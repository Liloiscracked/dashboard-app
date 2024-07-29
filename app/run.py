import sqlalchemy as sqlalchemy
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import pandas as pd
import plotly.express as px
import plotly.io as pio
import numpy as np
import plotly.graph_objects as go
import folium

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management
app.permanent_session_lifetime = timedelta(days=5)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn
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
        file1 = request.files["file1"]
        file2 = request.files["file2"]

        if file1 and file2:
            df1 = pd.read_csv(file1)
            df2 = pd.read_csv(file2)

            # Data Cleaning for the first file
            df1 = df1.dropna(subset=['Data Throughput-RLC DL Throughput (kbps)', 'RSRP Legend'])
            df1['Data Throughput-RLC DL Throughput (kbps)'].fillna(0, inplace=True)

            # Data Cleaning for the second file
            df2 = df2.dropna(subset=['Data Throughput-RLC DL Throughput (kbps)', 'RSRP Legend'])
            df2['Data Throughput-RLC DL Throughput (kbps)'].fillna(0, inplace=True)

            # Combine data from both files
            df_combined = pd.concat([df1, df2], ignore_index=True)

            # Visualization for File 1
            fig_map1 = px.scatter_mapbox(df1, lat="Latitude", lon="Longitude", color="RSRP Legend",
                                        size="Data Throughput-RLC DL Throughput (kbps)",
                                        color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
                                        mapbox_style="open-street-map",
                                        title="Network Coverage and Throughput - File 1")
            fig_map1.update_layout(autosize=True, margin=dict(l=0, r=0, t=40, b=0), width=1200, height=800)
            map_html1 = pio.to_html(fig_map1, full_html=False)

            fig_throughput1 = px.line(df1, x="Bin Time Stamp", y="Data Throughput-RLC DL Throughput (kbps)",
                                     title="Throughput Over Time - File 1", line_shape="linear", markers=True)
            fig_throughput1.update_layout(autosize=True, margin=dict(l=0, r=0, t=40, b=40), width=1200, height=400)
            throughput_html1 = pio.to_html(fig_throughput1, full_html=False)

            fig_rsrp1 = px.line(df1, x="Bin Time Stamp", y="Serving RS Info-Serving RSRP (d Bm)",
                               title="RSRP Over Time - File 1", line_shape="linear", markers=True)
            fig_rsrp1.update_layout(autosize=True, margin=dict(l=0, r=0, t=40, b=40), width=1200, height=400)
            rsrp_html1 = pio.to_html(fig_rsrp1, full_html=False)

            # Visualization for File 2
            fig_map2 = px.scatter_mapbox(df2, lat="Latitude", lon="Longitude", color="RSRP Legend",
                                        size="Data Throughput-RLC DL Throughput (kbps)",
                                        color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
                                        mapbox_style="open-street-map",
                                        title="Network Coverage and Throughput - File 2")
            fig_map2.update_layout(autosize=True, margin=dict(l=0, r=0, t=40, b=0), width=1200, height=800)
            map_html2 = pio.to_html(fig_map2, full_html=False)

            fig_throughput2 = px.line(df2, x="Bin Time Stamp", y="Data Throughput-RLC DL Throughput (kbps)",
                                     title="Throughput Over Time - File 2", line_shape="linear", markers=True)
            fig_throughput2.update_layout(autosize=True, margin=dict(l=0, r=0, t=40, b=40), width=1200, height=400)
            throughput_html2 = pio.to_html(fig_throughput2, full_html=False)

            fig_rsrp2 = px.line(df2, x="Bin Time Stamp", y="Serving RS Info-Serving RSRP (d Bm)",
                               title="RSRP Over Time - File 2", line_shape="linear", markers=True)
            fig_rsrp2.update_layout(autosize=True, margin=dict(l=0, r=0, t=40, b=40), width=1200, height=400)
            rsrp_html2 = pio.to_html(fig_rsrp2, full_html=False)

            # Render the template with the visualizations
            return render_template('index.html',
                                   map_html1=map_html1, throughput_html1=throughput_html1, rsrp_html1=rsrp_html1,
                                   map_html2=map_html2, throughput_html2=throughput_html2, rsrp_html2=rsrp_html2)
    else:
        return render_template("upload.html")
@app.route("/2g",methods = ["POST","GET"])
def two_g():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']

        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        polqa_html1 = generate_polqa_bar_chart(df1)
        polqa_html2 = generate_polqa_bar_chart(df2)

        rx_qual_html1 = generate_rx_qual_bar_chart(df1)
        rx_qual_html2 = generate_rx_qual_bar_chart(df2)

        gsm_power_html1 = generate_gsm_power_bar_chart(df1)
        gsm_power_html2 = generate_gsm_power_bar_chart(df2)

        def get_polqa_color(value):
            if value >= 4:
                return 'darkgreen'
            elif value >= 3:
                return 'lightgreen'
            elif value >= 2:
                return 'yellow'
            elif value >= 1:
                return 'orange'
            else:
                return 'red'

        def get_rx_qual_color(value):
            if value <= 3:
                return 'darkgreen'
            elif value <= 5:
                return 'yellow'
            elif value <= 7:
                return 'red'
            else:
                return 'black'

        def get_gsm_power_color(value):
            if value >= -65:
                return 'darkgreen'
            elif value >= -75:
                return 'lightgreen'
            elif value >= -85:
                return 'yellow'
            elif value >= -95:
                return 'orange'
            elif value >= -110:
                return 'red'
            else:
                return 'black'

        map_html1 = generate_folium_map(df1, 'Audio  Quality.POLQA Downlink MOS-POLQA NB', get_polqa_color)
        map_html2 = generate_folium_map(df2, 'Audio  Quality.POLQA Downlink MOS-POLQA NB', get_polqa_color)

        rx_qual_map_html1 = generate_folium_map(df1, 'GSM Rx Qual-GSM Serving Cell Rx Qual Sub', get_rx_qual_color)
        rx_qual_map_html2 = generate_folium_map(df2, 'GSM Rx Qual-GSM Serving Cell Rx Qual Sub', get_rx_qual_color)

        gsm_power_map_html1 = generate_folium_map(df1, 'GSM Power-GSM Serving Cell Rx Level Sub', get_gsm_power_color)
        gsm_power_map_html2 = generate_folium_map(df2, 'GSM Power-GSM Serving Cell Rx Level Sub', get_gsm_power_color)

        polqa_stats1 = calculate_statistics(df1, 'Audio  Quality.POLQA Downlink MOS-POLQA NB')
        polqa_stats2 = calculate_statistics(df2, 'Audio  Quality.POLQA Downlink MOS-POLQA NB')

        rx_qual_stats1 = calculate_statistics(df1, 'GSM Rx Qual-GSM Serving Cell Rx Qual Sub')
        rx_qual_stats2 = calculate_statistics(df2, 'GSM Rx Qual-GSM Serving Cell Rx Qual Sub')

        gsm_power_stats1 = calculate_statistics(df1, 'GSM Power-GSM Serving Cell Rx Level Sub')
        gsm_power_stats2 = calculate_statistics(df2, 'GSM Power-GSM Serving Cell Rx Level Sub')

        return render_template('2g.html',
                               polqa_html1=polqa_html1,
                               polqa_html2=polqa_html2,
                               map_html1=map_html1,
                               map_html2=map_html2,
                               rx_qual_html1=rx_qual_html1,
                               rx_qual_html2=rx_qual_html2,
                               rx_qual_map_html1=rx_qual_map_html1,
                               rx_qual_map_html2=rx_qual_map_html2,
                               gsm_power_html1=gsm_power_html1,
                               gsm_power_html2=gsm_power_html2,
                               gsm_power_map_html1=gsm_power_map_html1,
                               gsm_power_map_html2=gsm_power_map_html2,
                               polqa_stats1=polqa_stats1,
                               polqa_stats2=polqa_stats2,
                               rx_qual_stats1=rx_qual_stats1,
                               rx_qual_stats2=rx_qual_stats2,
                               gsm_power_stats1=gsm_power_stats1,
                               gsm_power_stats2=gsm_power_stats2)

    return render_template('2g.html', polqa_html1='', polqa_html2='', map_html1='', map_html2='',
                           rx_qual_html1='', rx_qual_html2='', rx_qual_map_html1='', rx_qual_map_html2='',
                           gsm_power_html1='', gsm_power_html2='', gsm_power_map_html1='', gsm_power_map_html2='',
                           polqa_stats1={}, polqa_stats2={}, rx_qual_stats1={}, rx_qual_stats2={},
                           gsm_power_stats1={}, gsm_power_stats2={})


if __name__ == "__main__":
    app.run(debug=True)
