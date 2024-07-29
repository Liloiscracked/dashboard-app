import pandas as pd
import plotly.express as px
import plotly.io as pio
import folium

class DataProcessor_2g:
    def __init__(self, file1, file2):
        self.df1 = pd.read_csv(file1)
        self.df2 = pd.read_csv(file2)
        self.process_data()
        self.generate_visualizations()

    def process_data(self):
        self.df1 = self.df1.dropna(
            subset=['Audio  Quality.POLQA Downlink MOS-POLQA NB', 'GSM Rx Qual-GSM Serving Cell Rx Qual Sub',
                    'GSM Power-GSM Serving Cell Rx Level Sub'])
        self.df2 = self.df2.dropna(
            subset=['Audio  Quality.POLQA Downlink MOS-POLQA NB', 'GSM Rx Qual-GSM Serving Cell Rx Qual Sub',
                    'GSM Power-GSM Serving Cell Rx Level Sub'])

        self.df1 = self.df1.fillna({
            'Audio  Quality.POLQA Downlink MOS-POLQA NB': 0,
            'GSM Rx Qual-GSM Serving Cell Rx Qual Sub': 0,
            'GSM Power-GSM Serving Cell Rx Level Sub': 0
        })
        self.df2 = self.df2.fillna({
            'Audio  Quality.POLQA Downlink MOS-POLQA NB': 0,
            'GSM Rx Qual-GSM Serving Cell Rx Qual Sub': 0,
            'GSM Power-GSM Serving Cell Rx Level Sub': 0
        })

    def calculate_statistics(self, df, column):
        return {
            'mean': df[column].mean(),
            'max': df[column].max(),
            'std': df[column].std()
        }

    def generate_bar_chart(self, df, column, bins, labels, colors):
        # Bin data and calculate percentages
        counts = pd.cut(df[column], bins=bins, labels=labels).value_counts(normalize=True) * 100
        counts = counts.reindex(labels, fill_value=0)  # Ensure all labels are present

        # Ensure colors correspond to the labels
        color_map = {label: color for label, color in zip(labels, colors)}

        fig = px.bar(
            x=counts.index.astype(str),
            y=counts.values,
            color=counts.index.astype(str),
            color_discrete_map=color_map
        )
        fig.update_layout(
            title=f'{column} Distribution',
            xaxis_title='Range',
            yaxis_title='Percentage (%)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        return pio.to_html(fig, full_html=False)

    def generate_folium_map(self, df, value_column, get_color):
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
        self.polqa_html1 = self.generate_bar_chart(
            self.df1,
            'Audio  Quality.POLQA Downlink MOS-POLQA NB',
            [1, 2, 3, 4, 5],
            ["1 to 2", "2 to 3", "3 to 4", "4 to 5"],
            ['red', 'yellow', 'lightgreen', 'darkgreen']
        )
        self.polqa_html2 = self.generate_bar_chart(
            self.df2,
            'Audio  Quality.POLQA Downlink MOS-POLQA NB',
            [1, 2, 3, 4, 5],
            ["1 to 2", "2 to 3", "3 to 4", "4 to 5"],
            ['red', 'yellow', 'lightgreen', 'darkgreen']
        )

        self.rx_qual_html1 = self.generate_bar_chart(
            self.df1,
            'GSM Rx Qual-GSM Serving Cell Rx Qual Sub',
            [0, 3, 5, 7, 20],
            ["0 to 3", "3 to 5", "5 to 7", "7 to 20"],
            ['darkgreen', 'yellow', 'red', 'black']
        )
        self.rx_qual_html2 = self.generate_bar_chart(
            self.df2,
            'GSM Rx Qual-GSM Serving Cell Rx Qual Sub',
            [0, 3, 5, 7, 20],
            ["0 to 3", "3 to 5", "5 to 7", "7 to 20"],
            ['darkgreen', 'yellow', 'red', 'black']
        )

        self.gsm_power_html1 = self.generate_bar_chart(
            self.df1,
            'GSM Power-GSM Serving Cell Rx Level Sub',
            [-150, -110, -95, -85, -75, -65, 0],
            ["-110 to -150", "-95 to -110", "-85 to -95", "-75 to -85", "-65 to -75", "0 to -65"],
            ['black', 'red', 'orange', 'yellow', 'lightgreen', 'darkgreen']
        )
        self.gsm_power_html2 = self.generate_bar_chart(
            self.df2,
            'GSM Power-GSM Serving Cell Rx Level Sub',
            [-150, -110, -95, -85, -75, -65, 0],
            ["-110 to -150", "-95 to -110", "-85 to -95", "-75 to -85", "-65 to -75", "0 to -65"],
            ['black', 'red', 'orange', 'yellow', 'lightgreen', 'darkgreen']
        )

        self.map_html1 = self.generate_folium_map(
            self.df1,
            'Audio  Quality.POLQA Downlink MOS-POLQA NB',
            self.get_polqa_color
        )
        self.map_html2 = self.generate_folium_map(
            self.df2,
            'Audio  Quality.POLQA Downlink MOS-POLQA NB',
            self.get_polqa_color
        )

        self.rx_qual_map_html1 = self.generate_folium_map(
            self.df1,
            'GSM Rx Qual-GSM Serving Cell Rx Qual Sub',
            self.get_rx_qual_color
        )
        self.rx_qual_map_html2 = self.generate_folium_map(
            self.df2,
            'GSM Rx Qual-GSM Serving Cell Rx Qual Sub',
            self.get_rx_qual_color
        )

        self.gsm_power_map_html1 = self.generate_folium_map(
            self.df1,
            'GSM Power-GSM Serving Cell Rx Level Sub',
            self.get_gsm_power_color
        )
        self.gsm_power_map_html2 = self.generate_folium_map(
            self.df2,
            'GSM Power-GSM Serving Cell Rx Level Sub',
            self.get_gsm_power_color
        )

        self.polqa_stats1 = self.calculate_statistics(self.df1, 'Audio  Quality.POLQA Downlink MOS-POLQA NB')
        self.polqa_stats2 = self.calculate_statistics(self.df2, 'Audio  Quality.POLQA Downlink MOS-POLQA NB')

        self.rx_qual_stats1 = self.calculate_statistics(self.df1, 'GSM Rx Qual-GSM Serving Cell Rx Qual Sub')
        self.rx_qual_stats2 = self.calculate_statistics(self.df2, 'GSM Rx Qual-GSM Serving Cell Rx Qual Sub')

        self.gsm_power_stats1 = self.calculate_statistics(self.df1, 'GSM Power-GSM Serving Cell Rx Level Sub')
        self.gsm_power_stats2 = self.calculate_statistics(self.df2, 'GSM Power-GSM Serving Cell Rx Level Sub')

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

    def get_rx_qual_color(self, value):
        if value <= 3:
            return 'darkgreen'
        elif value <= 5:
            return 'yellow'
        elif value <= 7:
            return 'red'
        else:
            return 'black'

    def get_gsm_power_color(self, value):
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
