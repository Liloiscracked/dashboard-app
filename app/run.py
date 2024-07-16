import sqlalchemy as sqlalchemy
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import csv
import plotly.express as px
import plotly.io as pio
import pandas as pd
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days= 5) # can be minutes days, etc....


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True # to make the session permanent !!
        user = request.form["nm"]
        session["user"] = user
        flash("Login successful !!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in")
            return redirect(url_for("home"))
        return render_template("login.html")

@app.route("/home")
def home():
    # Read the CSV file
    df = pd.read_csv("clustered_network_data.csv")

    # Data Cleaning
    df = df.dropna(subset=['Data Throughput-RLC DL Throughput (kbps)', 'RSRP Legend'])
    df['Data Throughput-RLC DL Throughput (kbps)'].fillna(0, inplace=True)
    # Get selected cluster and date range from the form, if any
    selected_cluster = request.args.get('cluster', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    if selected_cluster:
        df_filtered = df[df['Cluster'] == int(selected_cluster)]
    else:
        df_filtered = df

    if start_date and end_date:
        df_filtered = df_filtered[(df_filtered['Bin Time Stamp'] >= start_date) & (df_filtered['Bin Time Stamp'] <= end_date)]

    # Sample a subset of the data for the map visualization
    sample_size = min(1000, len(df_filtered))  # Ensure we do not sample more than available records
    df_sample = df_filtered.sample(n=sample_size, random_state=42)

    # Map Visualization
    fig_map = px.scatter_mapbox(df_sample, lat="Latitude", lon="Longitude", color="RSRP Legend",
                                size="Data Throughput-RLC DL Throughput (kbps)",
                                color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
                                mapbox_style="open-street-map",
                                title="Network Coverage and Throughput")

    fig_map.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=40, b=0),  # Add some space around the plot
        width=1200,
        height=800
    )

    map_html = pio.to_html(fig_map, full_html=False)

    # Line Chart for Throughput over Time
    fig_throughput = px.line(df_filtered, x="Bin Time Stamp", y="Data Throughput-RLC DL Throughput (kbps)",
                             title="Throughput Over Time", line_shape="linear", markers=True)

    fig_throughput.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=40, b=40),  # Add some space around the plot
        width=1200,
        height=400,
        title="Data Throughput Over Time"
    )

    throughput_html = pio.to_html(fig_throughput, full_html=False)

    # Line Chart for RSRP over Time
    fig_rsrp = px.line(df_filtered, x="Bin Time Stamp", y="Serving RS Info-Serving RSRP (d Bm)",
                       title="RSRP Over Time", line_shape="linear", markers=True)

    fig_rsrp.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=40, b=40),  # Add some space around the plot
        width=1200,
        height=400,
        title="RSRP Over Time"
    )

    rsrp_html = pio.to_html(fig_rsrp, full_html=False)

    # Get the unique clusters for the dropdown
    clusters = df['Cluster'].unique()

    return render_template('index.html', map_html=map_html, throughput_html=throughput_html, rsrp_html=rsrp_html, clusters=clusters, start_date=start_date, end_date=end_date)

@app.route("/upload",  methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        session.permanent = True # to make the session permanent !!
        file = request.form["file"]
        session["file"] = file
        return redirect(url_for("show"))
    else:
        if "file" in session:
            return redirect(url_for("show"))
        return render_template("login.html")

#@app.route("/visualize")
#def show():

if __name__ == "__main__":
    app.run(debug=True)
