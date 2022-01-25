import logging
import json

# itertools handles the cycling through palette colours
import itertools

# Intern
from common import DATA_FILE, leaderboard_settings

# Extern
# Bokeh
from bokeh.layouts import layout
from bokeh.plotting import figure, save, output_file
from bokeh.models import ColumnDataSource, RangeSlider, HoverTool, Range1d
from bokeh.io import curdoc
from bokeh.palettes import Dark2_5 as palette

DEBUG_YAML = False
DEBUG_PLOT = False
LOGGER = logging.getLogger(__name__)
output_file("./web/index.html")

curdoc().theme = "dark_minimal"

# Main
LOGGER.info("Opening data file ...")
with open(DATA_FILE, "r") as handle:
    leaderboard_data = json.load(handle)
LOGGER.info("Data file loaded.")


def transform(input_data):
    dates = []
    aoe2_rm = []
    aoe2_team_rm = []
    aoe2_ew = []
    aoe2_team_ew = []
    aoe2_unranked = []

    aoe4_custom = []
    aoe4_qm_1v1 = []
    aoe4_qm_2v2 = []
    aoe4_qm_3v3 = []
    aoe4_qm_4v4 = []

    for entry in input_data:
        if DEBUG_YAML:
            print(json.dumps(entry))

        dates.append(entry["date"])
        aoe2_rm.append(entry["aoe2"]["rm"]) if entry["aoe2"][
            "rm"
        ] is not None else aoe2_rm.append(float("nan"))
        aoe2_team_rm.append(entry["aoe2"]["team_rm"]) if entry["aoe2"][
            "team_rm"
        ] is not None else aoe2_team_rm.append(float("nan"))
        aoe2_ew.append(entry["aoe2"]["ew"]) if entry["aoe2"][
            "ew"
        ] is not None else aoe2_ew.append(float("nan"))
        aoe2_team_ew.append(entry["aoe2"]["team_ew"]) if entry["aoe2"][
            "team_ew"
        ] is not None else aoe2_team_ew.append(float("nan"))
        aoe2_unranked.append(entry["aoe2"]["unranked"]) if entry["aoe2"][
            "unranked"
        ] is not None else aoe2_unranked.append(float("nan"))
        aoe4_custom.append(entry["aoe4"]["custom"]) if entry["aoe4"][
            "custom"
        ] is not None else aoe4_custom.append(float("nan"))
        aoe4_qm_1v1.append(entry["aoe4"]["qm_1v1"]) if entry["aoe4"][
            "qm_1v1"
        ] is not None else aoe4_qm_1v1.append(float("nan"))
        aoe4_qm_2v2.append(entry["aoe4"]["qm_2v2"]) if entry["aoe4"][
            "qm_2v2"
        ] is not None else aoe4_qm_2v2.append(float("nan"))
        aoe4_qm_3v3.append(entry["aoe4"]["qm_3v3"]) if entry["aoe4"][
            "qm_3v3"
        ] is not None else aoe4_qm_3v3.append(float("nan"))
        aoe4_qm_4v4.append(entry["aoe4"]["qm_4v4"]) if entry["aoe4"][
            "qm_4v4"
        ] is not None else aoe4_qm_4v4.append(float("nan"))

    # create dict as basis for ColumnDataSource
    data = {
        "dates": dates,
        "aoe2_rm": aoe2_rm,
        "aoe2_team_rm": aoe2_team_rm,
        "aoe2_ew": aoe2_ew,
        "aoe2_team_ew": aoe2_team_ew,
        "aoe2_unranked": aoe2_unranked,
        "aoe4_custom": aoe4_custom,
        "aoe4_qm_1v1": aoe4_qm_1v1,
        "aoe4_qm_2v2": aoe4_qm_2v2,
        "aoe4_qm_3v3": aoe4_qm_3v3,
        "aoe4_qm_4v4": aoe4_qm_4v4,
    }

    if DEBUG_PLOT:
        print(data)

    return data


data = transform(leaderboard_data)

source = ColumnDataSource(data=data)

# create a color iterator
colors = itertools.cycle(palette)

plot = figure(
    x_range=data["dates"],
    y_range=Range1d(0, 250000),
    title="Player amount on AoE2:DE and AoE4 leaderboards plotted over time",
    x_axis_label="Date",
    y_axis_label="Amount of players on the leaderboard",
    width=1000,
    height=700,
    sizing_mode="stretch_width",
    toolbar_location="below",
)

plot.add_tools(
    HoverTool(
        tooltips=[
            ("Game:", "$name"),
            ("Players:", "$y{0,0}"),
            ("Date:", "@dates"),
        ],
        mode="mouse",
    )
)

# add multiple renderers
for line_setting in leaderboard_settings:
    plot.line(
        x="dates",
        y=f"{line_setting.game}_{line_setting.leaderboard}",
        source=source,
        legend_label=f"{line_setting.legend}",
        name=f"{line_setting.legend}",
        line_width=2,
        color=next(colors),
        alpha=1.0,
    )
    plot.circle(
        x="dates",
        y=f"{line_setting.game}_{line_setting.leaderboard}",
        source=source,
        fill_color="white",
        size=8,
        legend_label=f"{line_setting.legend}",
        name=f"{line_setting.legend}",
        alpha=1.0,
    )

# Set y-axis bounds
plot.yaxis.bounds = (0, 300000)

# Legend customization
# make graphs hideble
plot.legend.click_policy = "mute"

# move legend location
plot.legend.location = "bottom_right"
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
