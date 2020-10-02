import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from airbnb_analytics import price_by_rating_fig, avg_rating_fig, bed_price_rating_fig
from airbnb_property_details import property_by_type_fig, room_type_fig, property_type_count_figure, host_options, hosts

PROPERTY_DETAILS = html.Div([
    html.Div([
        html.P("Welcome to Airbnb", className="w3-xxxlarge"),
        dbc.NavLink('View Airbnb Analytics', href="/analytics", style={'text-decoration': 'underline'})
    ], className="w3-container w3-black w3-center"),
    html.Br(),
    html.Div([
        html.Div([
            html.P(" Set Price Range (in US Dollars (USD))"),
            dcc.RangeSlider(
                id='price-range-slider',
                allowCross=False,
                min=0,
                max=4000,
                step=1,
                value=[0, 4000],
                marks={
                    0: '0',
                    200: '200',
                    400: '400',
                    600: '600',
                    800: '800',
                    1000: '1000',
                    2000: '2000',
                    4000: '4000'
                }
            ),
            html.P(id="selected_price"),
        ], className="w3-full w3-container w3-sand"),
    ], className="w3-row w3-border"),
    html.Div([
        html.Div(dcc.Graph(id='property_by_type', figure=property_by_type_fig), className="w3-container w3-half"),
        html.Div(dcc.Graph(id='room_by_type', figure=room_type_fig), className="w3-container w3-half")
    ], className="w3-row w3-border"),
    dcc.Graph(id='property_type_count', figure=property_type_count_figure, style={"width": "100%"}),
    html.Div(id='property-details-container', style={"width": "100%"}),
    html.H3('Host Details', className='w3-center'),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='host',
                options=host_options,
                value=hosts.iloc[0]['host_id']
            ),
            html.Img(id='host_img', src=hosts.iloc[0]['host_picture_url'], style={
                'border-radius': '4px',
                'padding': '4px',
                'width': '450px',
                'height': '450px',
                'background-image': 'url(https://upload.wikimedia.org/wikipedia/commons/0/0a/No-image-available.png)',
            }, className='w3-round'),
        ], className='w3-col m4'),
        html.Div(id='host-details', className='w3-col m8')
    ], className='w3-row w-border')
], style={"height": "80vh", "width": "100%"})

PROPERTY_ANALYTICS = html.Div([
    html.Div([
        html.P("Welcome to Airbnb Analytics", className="w3-xxxlarge"),
        dbc.NavLink('View Property Details', href="/property-details", style={'text-decoration': 'underline'}),
    ],
        className="w3-row w3-container w3-black w3-center"),
    html.Br(),
    dcc.Graph(id='property_type_avg', figure=avg_rating_fig, style={"width": "100%"}),
    dcc.Graph(id='price_by_rating', figure=price_by_rating_fig, style={"width": "100%"}),
    dcc.Graph(id='3d_bed_price_rating', figure=bed_price_rating_fig, style={"width": "100%"}),
], style={"height": "80vh", "width": "100%"})
