import logging

# import datetime
# import pandas as pd

# itertools handles the cycling through palette colours
import itertools

# Intern
from scripts.common import PLOT_OUTPUT, leaderboard_settings
from scripts.dataframes import prepare_dataframes

# Extern
# Bokeh
from bokeh.layouts import layout
from bokeh.plotting import figure, save, output_file
from bokeh.models import (
    ColumnDataSource,
    RangeSlider,
    HoverTool,
    Range1d,
    DatetimeTickFormatter,
)
from bokeh.io import curdoc
from bokeh.palettes import Category20_20 as palette

DEBUG_YAML = False
DEBUG_PLOT = False
LOGGER = logging.getLogger(__name__)
output_file(PLOT_OUTPUT)

curdoc().theme = "dark_minimal"

# Main
df_activity, df_playerbase, df_platforms, df_country = prepare_dataframes()

source = ColumnDataSource(df_activity)

# create a color iterator
colors = itertools.cycle(palette)

plot = figure(
    # x_range=data["dates"],
    x_axis_type="datetime",
    y_range=Range1d(0, 250000),
    title="Player amount on AoE2:DE, AoE3:DE and AoE4 leaderboards"
    " plotted over time",
    x_axis_label="Date",
    y_axis_label="Amount of players on the leaderboard",
    width=1200,
    height=700,
    sizing_mode="stretch_width",
    toolbar_location="below",
)

plot.add_tools(
    HoverTool(
        tooltips=[
            ("Leaderboard", "$name"),
            ("Accounts", "$y{0,0}"),
            ("Date", "@dates{%d-%m-%Y}"),
        ],
        formatters={
            "@dates": "datetime",
        },
        mode="mouse",
    )
)

# add multiple renderers
for game, leaderboard, legend, _ in leaderboard_settings:
    plot.line(
        x="dates",
        y=f"{game}_{leaderboard}",
        source=source,
        legend_label=f"{legend}",
        name=f"{legend}",
        line_width=3,
        color=next(colors),
        alpha=1.0,
    )
    if game == "aoe2":
        plot.circle(
            x="dates",
            y=f"{game}_{leaderboard}",
            source=source,
            fill_color="white",
            size=11,
            line_color="black",
            legend_label=f"{legend}",
            name=f"{legend}",
            alpha=1.0,
        )
    elif game == "aoe3":
        plot.square(
            x="dates",
            y=f"{game}_{leaderboard}",
            source=source,
            fill_color="blue",
            size=13,
            line_color="black",
            legend_label=f"{legend}",
            name=f"{legend}",
            alpha=1.0,
        )
    elif game == "aoe4":
        plot.hex_dot(
            x="dates",
            y=f"{game}_{leaderboard}",
            source=source,
            fill_color="yellow",
            size=13,
            line_color="black",
            legend_label=f"{legend}",
            name=f"{legend}",
            alpha=1.0,
        )

# Set y-axis bounds
plot.yaxis.bounds = (0, 300000)

# Set datetime formatter
plot.xaxis.formatter = DatetimeTickFormatter(
    hours=["%d-%m-%Y"],
    days=["%d-%m-%Y"],
    months=["%d-%m-%Y"],
    years=["%d-%m-%Y"],
)

# Legend customization
# make graphs hideble
plot.legend.click_policy = "mute"

# move legend location
plot.legend.location = "top_left"
plot.legend.title = "Games"

# disable scientific format of y-axis
plot.left[0].formatter.use_scientific = False

# Hide toolbar
plot.toolbar.autohide = True

# set up RangeSlider
range_slider = RangeSlider(
    title="Adjust y-axis range",
    start=0,
    end=250000,
    step=25000,
    value=(plot.y_range.start, plot.y_range.end),
)
range_slider.js_link("value", plot.y_range, "start", attr_selector=0)
range_slider.js_link("value", plot.y_range, "end", attr_selector=1)

# create layout
layout = layout(
    [
        [plot],
        [range_slider],
    ]
)

# save the results
save(layout)
