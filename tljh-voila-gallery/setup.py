from setuptools import setup

setup(
    name="tljh-voila-gallery",
    entry_points={"tljh": ["voila_gallery = voila_gallery"]},
    py_modules=["tljh_voila_gallery"],
)


