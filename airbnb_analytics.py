import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('listings_details.csv')
df.head()
external_stylesheets = ['https://www.w3schools.com/w3css/4/w3.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, routes_pathname_prefix="/airbnb-analytics/")

df['price_num'] = df['price'].replace('\$', '', regex=True).astype(str)
df['price_num'] = df['price_num'].replace('\,', '', regex=True).astype(float)

# room_type by location
df['property_details'] = df["neighbourhood"] + "," + df["state"] + "," + df["room_type"] + "," + \
                         df["price"]

# Avg rating (property_Type)
avg_rating_df = df.groupby('property_type').mean().reset_index()
avg_rating_fig = px.bar(avg_rating_df, title="Average Customer Rating of Each Property", x='property_type',
                        y='review_scores_rating')

# price by rating
price_by_rating_fig = px.bar(avg_rating_df, title="Average Customer Rating of Each Property", x='review_scores_rating',
                             y='price_num', text='price_num')

# 3D bed vs price vs rating
bed_price_rating_fig = px.scatter_3d(df, x=df['review_scores_rating'], y=df['price_num'], z=df['beds'],
                                     color=df['property_type'], symbol=df['room_type'])

app.layout = html.Div([
    html.Div([
        html.P("Welcome to Airbnb Analytics", className="w3-xxxlarge")
    ], className="w3-container w3-black w3-center"),
    html.Br(),
    dcc.Graph(id='property_type_avg', figure=avg_rating_fig, style={"width": "100%"}),
    dcc.Graph(id='price_by_rating', figure=price_by_rating_fig, style={"width": "100%"}),
    dcc.Graph(id='3d_bed_price_rating', figure=bed_price_rating_fig, style={"width": "100%"}),
], style={"height": "80vh", "width": "100%"})

if __name__ == '__main__':
    app.run_server(debug=True, port=7000)
