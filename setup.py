from setuptools import setup, find_packages

setup(
    name="aoe_playerbase_stats",
    version="0.3.1",
    description="Player amount on AoE2:DE and AoE4 leaderboards plotted over"
    " time",
    url="https://github.com/simonsan/aoe_playerbase_stats",
    packages=find_packages(),
    package_data={"aoe_playerbase_stats": ["data/*"]},
    install_requires=[
        "bokeh>=2.4.2",
        "aiohttp>=3.8.1",
        "pycountry>=22.1.10",
        "pandas>=1.4.0",
        "pyarrow>=6.0.1",
    ],
)
