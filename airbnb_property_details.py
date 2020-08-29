import math

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

import layout

df = pd.read_csv('listings_details.csv')
df.head()

external_stylesheets = ['https://www.w3schools.com/w3css/4/w3.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
app.title = "AirBnb Analytics"

# changing price to float
df['price_num'] = df['price'].replace('\$', '', regex=True).astype(str)
df['price_num'] = df['price_num'].replace('\,', '', regex=True).astype(float)

hosts = df[
    ['host_id', 'host_name', 'host_url', 'host_since', 'host_about', 'host_response_time', 'host_response_rate',
     'host_acceptance_rate', 'host_is_superhost', 'host_thumbnail_url', 'host_picture_url', 'host_neighbourhood',
     'host_total_listings_count', 'host_identity_verified', 'host_location']].drop_duplicates(subset=['host_id'])
host_options = []
for i in range(len(hosts)):
    host_options.append(
        {
            'label': str(hosts.iloc[i]['host_id']) + ' ' + str(hosts.iloc[i]['host_name']),
            'value': i
        }
    )

# property_type by location
property_by_type_fig = px.scatter_mapbox(df,
                                         title="Property Type in your City (Click on the property to get details)",
                                         lat=df['latitude'], lon=df['longitude'],
                                         hover_name=df['name'],
                                         color=df['property_type'], zoom=10)
property_by_type_fig.update_layout(mapbox_style="open-street-map")

# room_type by location
room_type_fig = px.scatter_mapbox(df,
                                  title="Room Type in your City (Click on the property to get details)",
                                  lat=df['latitude'], lon=df['longitude'],
                                  hover_name=df['name'],
                                  color=df['room_type'], zoom=10)
room_type_fig.update_layout(mapbox_style="open-street-map")

# property_type count
property_type_count_dataframe = df.groupby(['property_type']).size().reset_index(name='count')
property_type_count_figure = px.bar(property_type_count_dataframe, title="No. of Properties Available",
                                    x='property_type', y='count', text='count')
property_type_count_figure.update_traces(textposition='outside')

# Rating by price
avg_rating_fig = px.bar(df, x='property_type', y='review_scores_rating')

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

app.layout = url_bar_and_content_div


@app.callback(
    [Output('property_by_type', 'figure'),
     Output('room_by_type', 'figure'),
     Output('selected_price', 'children'),
     Output('property_type_count', 'figure')],
    [Input('price-range-slider', 'value')])
def update_property_by_price(value):
    if value is not None:
        price_df = df[(df['price_num'] >= value[0]) & (df['price_num'] <= value[1])]

        # Update Map Property Type
        property_by_type_fig = px.scatter_mapbox(price_df,
                                                 title="Property Type in your City (Click on the property to get details)",
                                                 lat=price_df['latitude'], lon=price_df['longitude'],
                                                 hover_name=price_df['name'],
                                                 color=price_df['property_type'], zoom=10)
        property_by_type_fig.update_layout(mapbox_style="open-street-map")

        # Update Map Room Type
        room_type_fig = px.scatter_mapbox(price_df,
                                          title="Room Type in your City (Click on the property to get details)",
                                          lat=price_df['latitude'], lon=price_df['longitude'],
                                          hover_name=price_df['name'],
                                          color=price_df['room_type'], zoom=10)
        room_type_fig.update_layout(mapbox_style="open-street-map")

        # Display Range
        price_range = "Filtering for price between ${} - ${}".format(value[0], value[1])

        # Update Table
        property_type_count_dataframe = price_df.groupby(['property_type']).size().reset_index(name='count')
        property_type_count_figure = px.bar(property_type_count_dataframe, title="No. of Properties Available",
                                            x='property_type', y='count', text='count')
        property_type_count_figure.update_traces(textposition='outside')
        return property_by_type_fig, room_type_fig, price_range, property_type_count_figure


@app.callback(
    Output('property-details-container', 'children'),
    [Input('property_by_type', 'clickData'),
     Input('room_by_type', 'clickData')])
def get_property_details(property_clickData, room_clickData):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'property_by_type' in changed_id:
        data = property_clickData['points'][0]['hovertext']
        property_click_dataframe = df.loc[df['name'] == data]
        return html.Div(
            [
                html.Br(),
                html.H3("Property Details"),
                html.Br(),
                html.Img(src=property_click_dataframe.iloc[0]['picture_url'], style={"width": "100%"}),
                html.Div([
                    html.P("To book Visit - {}".format(property_click_dataframe.iloc[0]['listing_url'])),
                    html.H4(html.B("Name")),
                    html.P(property_click_dataframe.iloc[0]['name']),
                    html.H4(html.B("Price")),
                    html.P(property_click_dataframe.iloc[0]['price']),
                    html.H4(html.B("Room Type")),
                    html.P(property_click_dataframe.iloc[0]['room_type']),
                    html.H4(html.B("Neighbourhood")),
                    html.P(property_click_dataframe.iloc[0]['neighbourhood']),
                    html.H4(html.B("Summary")),
                    html.P(property_click_dataframe.iloc[0]['summary']),
                    html.H4(html.B("Description")),
                    html.P(property_click_dataframe.iloc[0]['description']),
                    html.H4(html.B("Rating")),
                    html.P("{}/100".format(property_click_dataframe.iloc[0]['review_scores_rating'])),
                ], className="w3-container")
            ], className="w3-card-4"
        )
    elif 'room_by_type' in changed_id:
        data = room_clickData['points'][0]['hovertext']
        room_click_dataframe = df.loc[df['name'] == data]
        return html.Div(
            [
                html.Br(),
                html.H3("Property Details"),
                html.Br(),
                html.Img(src=room_click_dataframe.iloc[0]['picture_url'], style={"width": "100%"}),
                html.Div([
                    html.P("To book Visit - {}".format(room_click_dataframe.iloc[0]['listing_url'])),
                    html.H4(html.B("Name")),
                    html.P(room_click_dataframe.iloc[0]['name']),
                    html.H4(html.B("Price")),
                    html.P(room_click_dataframe.iloc[0]['price']),
                    html.H4(html.B("Room Type")),
                    html.P(room_click_dataframe.iloc[0]['room_type']),
                    html.H4(html.B("Neighbourhood")),
                    html.P(room_click_dataframe.iloc[0]['neighbourhood']),
                    html.H4(html.B("Summary")),
                    html.P(room_click_dataframe.iloc[0]['summary']),
                    html.H4(html.B("Description")),
                    html.P(room_click_dataframe.iloc[0]['description']),
                    html.H4(html.B("Rating")),
                    html.P("{}/100".format(room_click_dataframe.iloc[0]['review_scores_rating'])),
                ], className="w3-container")
            ], className="w3-card-4"
        )


@app.callback([Output('host_img', 'src'),
               Output('host-details', 'children')],
              [Input('host', 'value')])
def get_host_details(index):
    if hosts.iloc[index]['host_identity_verified'] == 't':
        verified_img = "https://banner2.cleanpng.com/20180611/sfq/kisspng-social-media-instagram-verified-badge" \
                       "-symbol-compu-5b1eedb5aba638.1612204615287535897031.jpg "
    else:
        verified_img = ''
    host_listings = df[df['host_id'] == hosts.iloc[index]['host_id']]
    host_listings.dropna()
    host_listings['rating_overall'] = host_listings['review_scores_rating'].map(
        lambda x: '⭐ ⭐ ⭐ ⭐ ⭐' if math.ceil((x - 5) / 5) == 5 else (
            '⭐ ⭐ ⭐ ⭐' if math.ceil((x - 5) / 5) == 4 else ('⭐ ⭐ ⭐' if math.ceil((x - 5) / 5) < 4 else '⭐ ⭐')))
    return hosts.iloc[index]['host_picture_url'], \
           html.Div([
               html.H2(hosts.iloc[index]['host_name'], className='w3-text-dark-grey'),
               html.Img(src=verified_img, alt='Not verified', style={
                   'height': '10px',
                   'width': '20px'
               }, className='w3-round'),
               html.P('Locations: ' + hosts.iloc[index]['host_location']),
               html.P(hosts.iloc[index]['host_about']),
               html.P('Total listings: ' + str(hosts.iloc[index]['host_total_listings_count'])),
               html.P('For full details visit: ' + hosts.iloc[index]['host_url']),
               html.B('Hosted Properties', className='w3-center'),
               dash_table.DataTable(
                   data=host_listings.to_dict('records'),
                   columns=[{"name": 'name', 'id': 'name'}, {'name': 'state', 'id': 'state'},
                            {'name': 'price', 'id': 'price'}, {'name': 'property type', 'id': 'property_type'},
                            {'name': 'Room type', 'id': 'room_type'}, {'name': 'book now @', 'id': 'listing_url'},
                            {'name': 'Rating', 'id': 'rating_overall'}],
                   page_size=10,
                   style_cell={
                       'height': 'auto',
                       'minWidth': '80px', 'width': '180px', 'maxWidth': '200px',
                       'whiteSpace': 'normal',
                       'textAlign': 'center'
                   },
                   style_table={'overflowX': 'auto'}
               )
           ], className='w3-card w3-margin w3-padding')


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/analytics":
        return layout.PROPERTY_ANALYTICS
    if pathname == "/property-details":
        return layout.PROPERTY_DETAILS
    return layout.PROPERTY_DETAILS


if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
