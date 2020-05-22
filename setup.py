from os import path
from setuptools import setup

DISTNAME = "awherepy"
DESCRIPTION = (
    "Python package built to retrieve, extract, and format"
    "weather and agronomic data from the aWhere API."
)
MAINTAINER = "Cale Kochenour"
MAINTAINER_EMAIL = "cale.kochenour@alumni.psu.edu"


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

if __name__ == "__main__":
    setup(
        name=DISTNAME,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        version="0.1.0",
        packages=["awherepy"],
        install_requires=[
            "matplotlib",
            "numpy",
            "seaborn",
            "geopandas",
            "earthpy",
            "shapely",
            "rasterstats",
            "descartes",
        ],
        zip_safe=False,
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python",
            "Topic :: Software Development",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Operating System :: MacOS",
        ],
        package_data={
            DISTNAME: [
                "tests/test-data/*.cpg",
                "tests/test-data/*.dbf",
                "tests/test-data/*.prj",
                "tests/test-data/*.shp",
                "tests/test-data/*.shx",
                "tests/test-data/*.xml",
                "tests/test-data/*.tfw",
                "tests/test-data/*.tif",
                "tests/test-data/*.tif.aux.xml",
                "tests/test-data/*.tif.ovr",
                "tests/test-data/*.tif.xml",
            ]
        },
        url="https://github.com/calekochenour/awherepy",
    )
