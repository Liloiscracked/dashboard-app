import sqlalchemy as sqlalchemy
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import pandas as pd
import plotly.express as px
import plotly.io as pio
import numpy as np

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management
app.permanent_session_lifetime = timedelta(days=5)

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash("Login successful !!")
        return redirect(url_for("home"))
    else:
        if "user" in session:
            flash("Already logged in")
            return redirect(url_for("home"))
        return render_template("login.html")

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

if __name__ == "__main__":
    app.run(debug=True)
