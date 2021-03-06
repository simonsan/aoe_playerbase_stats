from setuptools import setup, find_packages

setup(
    name="compare_leaderboards",
    version="0.3.1",
    description="Player amount on AoE2:DE and AoE4 leaderboards plotted over"
    " time",
    url="https://github.com/simonsan/leaderboard_comparison",
    packages=find_packages(),
    package_data={"compare_leaderboards": ["data/*"]},
    install_requires=[
        "bokeh>=2.4.2",
        "aiohttp>=3.8.1",
    ],
)
