import plotly.express as px
def create_chart(data):
    fig = px.line(data, x='date', y='value', title='Sample Chart')
    return fig.to_html()
