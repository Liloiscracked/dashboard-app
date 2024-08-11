import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
import plotly.io as pio


class DataProcessor_4g:
    def __init__(self, file):
        self.df = pd.read_csv(file, nrows=300)
        self.process_data()
        self.generate_visualizations()

    def process_data(self):
        self.df.dropna(subset=['Serving RS Info-Serving RSRP (d Bm)', 'Serving RS Info-Serving RSRQ (d B)',
                               'Serving Channel Info-DL EARFCN', 'Serving RS Info-Serving RS CINR (d B)',
                               'Audio Quality.POLQA Downlink MOS-POLQA SWB', ], inplace=True)

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

    def generate_pie_chart(self, df, column):
        counts = df[column].value_counts()
        colors = ['red', 'blue', 'green', 'purple', 'orange']
        fig = go.Figure(data=[go.Pie(labels=counts.index, values=counts.values,
                                     marker=dict(colors=colors))])
        fig.update_layout(title_text=f'Distribution of {column}')
        return pio.to_html(fig, full_html=False)

    def generate_visualizations(self):
        self.rsrp_html = self.generate_bar_chart(
            self.df,
            'Serving RS Info-Serving RSRP (d Bm)',
            [-120, -105, -95, -85, -75, float('inf')],
            ["-120 to -105", "-105 to -95", "-95 to -85", "-85 to -75", "-75 and above"],
            ['black', 'red', 'orange', 'yellow', 'lightgreen', 'darkgreen']
        )
        self.cinr_html = self.generate_bar_chart(
            self.df,
            'Serving RS Info-Serving RS CINR (d B)',
            [-10, 0, 5, 10, float('inf')],
            ["-10 to 0", "0 to 5", "5 to 10", "10 and above"],
            ['red', 'orange', 'yellow', 'lightgreen', 'darkgreen']
        )
        self.rsrq_html = self.generate_bar_chart(
            self.df,
            'Serving RS Info-Serving RSRQ (d B)',
            [-18, -14, -12, -10, -6, float('inf')],
            ["-18 to -14", "-14 to -12", "-12 to -10", "-10 to -6", "-6 and above"],
            ['black', 'red', 'orange', 'yellow', 'lightgreen', 'darkgreen']
        )
        self.polqa_html = self.generate_bar_chart(
            self.df,
            'Audio Quality.POLQA Downlink MOS-POLQA SWB',
            [0, 1, 2, 3, 4, 5],
            ["0 to 1", "1 to 2", "2 to 3", "3 to 4", "4 to 5"],
            ['red', 'orange', 'yellow', 'lightgreen', 'darkgreen']
        )
        self.rsrp_map_html = self.generate_map(
            self.df,
            'Serving RS Info-Serving RSRP (d Bm)',
            self.get_rsrp_color
        )
        self.cinr_map_html = self.generate_map(
            self.df,
            'Serving RS Info-Serving RS CINR (d B)',
            self.get_cinr_color
        )
        self.rsrq_map_html = self.generate_map(
            self.df,
            'Serving RS Info-Serving RSRQ (d B)',
            self.get_rsrq_color
        )
        self.polqa_map_html = self.generate_map(
            self.df,
            'Audio Quality.POLQA Downlink MOS-POLQA SWB',
            self.get_polqa_color
        )
        self.earfcn_pie_html = self.generate_pie_chart(
            self.df,
            'Serving Channel Info-DL EARFCN'
        )
        self.earfcn_map_html = self.generate_map(
            self.df,
            'Serving Channel Info-DL EARFCN',
            self.get_earfcn_color
        )

    def get_rsrp_color(self, value):
        if value >= -75:
            return 'darkgreen'
        elif value >= -85:
            return 'lightgreen'
        elif value >= -95:
            return 'yellow'
        elif value >= -105:
            return 'orange'
        elif value >= -120:
            return 'red'
        else:
            return 'black'

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

    def get_rsrq_color(self, value):
        if value >= -6:
            return 'darkgreen'
        elif value >= -10:
            return 'lightgreen'
        elif value >= -12:
            return 'yellow'
        elif value >= -14:
            return 'orange'
        elif value >= -18:
            return 'red'
        else:
            return 'black'

    def get_polqa_color(self, value):
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

    def get_earfcn_color(self, value):
        distinct_values = self.df['Serving Channel Info-DL EARFCN'].unique()
        colors = ['red', 'blue', 'green', 'purple', 'orange']
        color_dict = {val: colors[i % len(colors)] for i, val in enumerate(distinct_values)}
        return color_dict.get(value, 'gray')
