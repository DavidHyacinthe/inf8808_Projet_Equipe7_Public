'''
    Contains the template to use in the data visualization.
'''
import plotly.graph_objects as go
import plotly.io as pio


THEME = {
    'background_color': '#2A2B2E',
    'font_family': 'Grenze Gotish',
    'accent_font_family': 'Grenze Gotish',
    'dark_color': '#2A2B2E',
    'pale_color': '#DFD9E2',
    'line_chart_color': 'black',
    'label_font_size': 14,
    'label_background_color': '#ffffff',
    'colorscale': 'Bluyl',
    'axis' : 'white',
    'tick_font_size': 15,
    'title_font_size': 18
}

COLORS = {'oscar_base': '#d545f4',
          'oscar_light': '#e8bef4',
          'oscar_dark': '#8609a1',
          'globe_base': '#f5c136', 
          'globe_light': '#ffdf89',
          'globe_dark': '#bd8d0a',
          'both_base': '#44ed1b',
          'unimportant': '#706a69'}


def create_custom_theme():
    '''
        Adds a new layout template to pio's templates.

    '''
    # Add a new layout template
    custom_theme = go.layout.Template()

    # Set the font color and the font family
    custom_theme.layout.font.color = THEME['pale_color']
    custom_theme.layout.font.family = THEME['font_family']

    # Set the plot background and the paper background
    custom_theme.layout.paper_bgcolor = THEME['background_color']
    custom_theme.layout.plot_bgcolor = THEME['background_color']

    # Set the hover label
    custom_theme.layout.hoverlabel.bgcolor = THEME['label_background_color']
    custom_theme.layout.hoverlabel.font.size = THEME['label_font_size']
    custom_theme.layout.hoverlabel.font.color = THEME['dark_color']
    custom_theme.layout.hovermode = 'closest'

    # Set the line chart's line color
    custom_theme.layout.colorway = [THEME['line_chart_color']]

    # Set the color scale of the heatmap
    custom_theme.layout.colorscale.sequential = THEME['colorscale']

    # Set frame's line color to white
    custom_theme.layout.xaxis.showline = True
    custom_theme.layout.xaxis.linecolor = THEME['axis']
    custom_theme.layout.yaxis.showline = True
    custom_theme.layout.yaxis.linecolor = THEME['axis']
    custom_theme.layout.xaxis.tickfont.size = THEME['tick_font_size']
    custom_theme.layout.xaxis.titlefont.size = THEME['title_font_size']

    custom_theme.layout.xaxis.gridcolor = THEME['axis']
    custom_theme.layout.yaxis.gridcolor = THEME['axis']
    custom_theme.layout.yaxis.tickfont.size = THEME['tick_font_size']
    custom_theme.layout.yaxis.titlefont.size = THEME['title_font_size']

    custom_theme.layout.legend.font.size = THEME['tick_font_size']


    pio.templates['custom_theme'] = custom_theme


def set_default_theme():
    '''
        Sets the default theme to be a combination of the
        'plotly_white' theme and our custom theme.
    '''
    # Set default theme
    pio.templates.default = 'plotly_white+custom_theme'