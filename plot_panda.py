import logging

# import datetime
# import pandas as pd

# itertools handles the cycling through palette colours
import itertools

# Intern
from scripts.common import PLOT_OUTPUT, leaderboard_settings, ACTIVITY_PERIODS
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
    CustomJS,
    MultiChoice,
    Div,
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

activity_plot = figure(
    x_axis_type="datetime",
    y_range=Range1d(0, 175000),
    title="Player amount on AoE2:DE, AoE3:DE and AoE4 leaderboards"
    " plotted over time",
    x_axis_label="Date",
    y_axis_label="Amount of players on the leaderboard",
    width=1200,
    height=700,
    sizing_mode="stretch_width",
    toolbar_location="below",
)

activity_plot.add_tools(
    HoverTool(
        tooltips=[
            ("Leaderboard", "$name"),
            ("Accounts", "$y{0,0}"),
            ("Date", "@timestamp{%d-%m-%Y}"),
        ],
        formatters={
            "@timestamp": "datetime",
        },
        mode="mouse",
    )
)

# add multiple renderers
for game, leaderboard, legend, _ in leaderboard_settings:
    for activity in ACTIVITY_PERIODS:
        activity_plot.line(
            x="timestamp",
            y=f"leaderboard_activity_{activity}_{game}_{leaderboard}",
            source=source,
            legend_label=f"{legend} {activity}",
            name=f"{legend} {activity}",
            line_width=3,
            color=next(colors),
            alpha=1.0,
        )
        if game == "aoe2":
            activity_plot.circle(
                x="timestamp",
                y=f"leaderboard_activity_{activity}_{game}_{leaderboard}",
                source=source,
                fill_color="white",
                size=11,
                line_color="black",
                legend_label=f"{legend} {activity}",
                name=f"{legend} {activity}",
                alpha=1.0,
            )
        elif game == "aoe3":
            activity_plot.square(
                x="timestamp",
                y=f"leaderboard_activity_{activity}_{game}_{leaderboard}",
                source=source,
                fill_color="blue",
                size=13,
                line_color="black",
                legend_label=f"{legend} {activity}",
                name=f"{legend} {activity}",
                alpha=1.0,
            )
        elif game == "aoe4":
            activity_plot.hex_dot(
                x="timestamp",
                y=f"leaderboard_activity_{activity}_{game}_{leaderboard}",
                source=source,
                fill_color="yellow",
                size=13,
                line_color="black",
                legend_label=f"{legend} {activity}",
                name=f"{legend} {activity}",
                alpha=1.0,
            )

# Set y-axis bounds
activity_plot.yaxis.bounds = (0, 225000)

# Set datetime formatter
activity_plot.xaxis.formatter = DatetimeTickFormatter(
    hours=["%d-%m-%Y"],
    days=["%d-%m-%Y"],
    months=["%d-%m-%Y"],
    years=["%d-%m-%Y"],
)

# Legend customization
# make graphs hideble
activity_plot.legend.click_policy = "mute"

# move legend location
activity_plot.legend.location = "top_left"
activity_plot.legend.title = "Games"

# disable scientific format of y-axis
activity_plot.left[0].formatter.use_scientific = False

# Hide toolbar
activity_plot.toolbar.autohide = True

# set up RangeSlider
range_slider = RangeSlider(
    title="Adjust y-axis range",
    start=0,
    end=200000,
    step=15000,
    value=(activity_plot.y_range.start, activity_plot.y_range.end),
)
range_slider.js_link("value", activity_plot.y_range, "start", attr_selector=0)
range_slider.js_link("value", activity_plot.y_range, "end", attr_selector=1)

multi_choice = MultiChoice(value=["30d"], options=ACTIVITY_PERIODS)
multi_choice.js_on_change(
    "value",
    CustomJS(
        code="""
    console.log('multi_choice: value=' + this.value, this.toString())
"""
    ),
)

explanations = Div(
    text="""This project is not endorsed by or affiliated with Microsoft in
     any way. With data from AoE2/3/IV.net. For more information check the
     <a href='https://github.com/simonsan/aoe_playerbase_stats'>Github
     Repository</a>.""",
    width=200,
    height=100,
)

# create layout
layout = layout(
    [
        [activity_plot],
        [range_slider],
        [multi_choice],
        [explanations],
    ]
)

# save the results
save(layout)
