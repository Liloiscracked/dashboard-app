import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
import plotly.io as pio


class DataProcessor_5g:
    def __init__(self, file):
        self.df = pd.read_csv(file)
        self.process_data()
        self.generate_visualizations()

    def process_data(self):
        self.df.dropna(subset=['RSRP (d Bm)-Dominant RSRP (d Bm) ','Data Throughput-NR PDCP downlink throughput (Mbps)', 'Serving RS Info-NR Best SS-SINR'], inplace=True)

    def stats(self, feature):
        return [self.df[feature].min(), self.df[feature].max(), self.df[feature].mean(), self.df[feature].std()]

    def generate_bar_chart(self, df, column, bins, labels, colors):
        if len(bins) != len(labels) + 1:
            raise ValueError("Bins must be one more than the number of labels")

        dic = {label: 0 for label in labels}
        length = len(df)

        for val in df[column]:
            for i in range(1, len(bins)):
                if bins[i - 1] <= val < bins[i]:
                    dic[labels[i - 1]] += 1
                    break
            else:
                if val >= bins[-1]:
                    dic[labels[-1]] += 1

        dic = {k: round(v / length * 100, 2) for k, v in dic.items()}

        fig = go.Figure()

        for i, (label, color) in enumerate(zip(dic.keys(), colors)):
            fig.add_trace(
                go.Bar(
                    x=[label],
                    y=[dic[label]],
                    name=label,
                    marker_color=color
                )
            )

        fig.update_layout(
            title=f'{column} Distribution',
            xaxis_title='Range',
            yaxis_title='Percentage (%)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )

        return pio.to_html(fig, full_html=False)

    def generate_map(self, df, value_column, get_color):
        folium_map = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=5,
                color=get_color(row[value_column]),
                fill=True,
                fill_color=get_color(row[value_column]),
                fill_opacity=0.7,
                popup=f"{value_column}: {row[value_column]}"
            ).add_to(folium_map)
        return folium_map._repr_html_()

    def generate_visualizations(self):
        self.rsrp_html = self.generate_bar_chart(
            self.df,
            'RSRP (d Bm)-Dominant RSRP (d Bm) ',
            [-180,-120, -105, -95, -85, 0],
            ["-180 to -120", "-120 to -105", "-105 to -95", "-95 to -85", "-85 to 0"],
            ['red', 'orange', 'yellow', 'lightgreen', 'darkgreen']
        )
        self.cinr_html = self.generate_bar_chart(
            self.df,
            'Serving RS Info-NR Best SS-SINR',
            [-20, -10,0, 5, 10, 50],
            ["-20 to -10", "-10 to 0", "0 to 5", "5 to 10", "10 to 50"],
            ['red', 'orange', 'yellow', 'lightgreen', 'darkgreen']
        )
        self.dl_html = self.generate_bar_chart(
            self.df,
            'Data Throughput-NR PDCP downlink throughput (Mbps)',
            [0, 25, 50, 100, 200, 500, 1500],
            ["0 to 25", "25 to 50", "50 to 100", "100 to 200", "200 to 500", "500 to 1500"],
            ['red', 'orange', 'yellow', 'lightgreen', 'darkgreen', 'blue']
        )
        self.rsrp_map_html = self.generate_map(
            self.df,
            'RSRP (d Bm)-Dominant RSRP (d Bm) ',
            self.get_rsrp_color
        )
        self.cinr_map_html = self.generate_map(
            self.df,
            'Serving RS Info-NR Best SS-SINR',
            self.get_cinr_color
        )
        self.dl_map_html = self.generate_map(
            self.df,
            'Data Throughput-NR PDCP downlink throughput (Mbps)',
            self.get_dl_color
        )


    def get_rsrp_color(self, value):
        if value >= -85:
            return 'darkgreen'
        elif value >= -95:
            return 'lightgreen'
        elif value >= -105:
            return 'yellow'
        elif value >= -120:
            return 'orange'
        else:
            return 'red'

    def get_cinr_color(self, value):
        if value >= 10:
            return 'darkgreen'
        elif value >= 5:
            return 'lightgreen'
        elif value >= 0:
            return 'yellow'
        elif value >= -10:
            return 'orange'
        else:
            return 'red'

    def get_dl_color(self, value):
        if value >= 500:
            return 'blue'
        elif value >= 200:
            return 'darkgreen'
        elif value >= 100:
            return 'lightgreen'
        elif value >= 50:
            return  'yellow'
        elif value >= 25:
            return 'orange'
        else:
            return 'red'
