from setuptools import setup, find_packages

setup(
    name="tljh-voila-gallery",
    entry_points={"tljh": ["tljh_voila_gallery = tljh_voila_gallery"]},
    packages=find_packages(),
    include_package_data=True
)
