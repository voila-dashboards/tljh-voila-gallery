# Voila Gallery

This is a gallery of [voila](https://github.com/QuantStack/voila)
examples. Use this for inspiration on using voila and
[ipywidgets](https://github.com/jupyter-widgets/ipywidgets).

## Contributing new examples

1. Create a repository with your notebook. You can copy the [gaussian-density](https://github.com/voila-gallery/gaussian-density) example.
2. Test your repository on Binder.
3. Create a PR to [voila-gallery](https://github.com/voila-gallery/gallery) that
   modifies `tljh-voila-gallery/tljh_voila_gallery/gallery.yaml`.
   You will need to fill in the following fields:
   - title: the title used in the page thumbnail.
   - description: the description used in the page thumbnail.
   - image: the name of the built Docker image. This should be `$title:latest`.
   - url: the URL of the notebook to render.
   - repo_url: the URL of the repository serving as source.
   - image_url: the URL of the picture to use as thumbnail.
