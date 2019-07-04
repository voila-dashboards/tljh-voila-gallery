# Voila Gallery

This is a gallery of [voila](https://github.com/QuantStack/voila)
examples. Use this for inspiration on using voila and
[ipywidgets](https://github.com/jupyter-widgets/ipywidgets).

View the gallery at [voila-gallery.org](http://voila-gallery.org).

## Going back to the gallery screen

You can go back to the gallery landing page using the back button of the web browser.

## Contributing new examples

1. Create a repository with your notebook. You can start from the [hello-world](https://github.com/voila-gallery/hello-world-example) example.
2. The gallery launches the examples using Docker containers, similar to what Binder does. This means that [the repository can be first tested on Binder](https://mybinder.readthedocs.io/en/latest/introduction.html#preparing-a-repository-for-binder).
2. Test your repository on Binder.
3. Create a PR to [voila-gallery](https://github.com/voila-gallery/gallery) that
   modifies `tljh-voila-gallery/tljh_voila_gallery/gallery.yaml`.
   You will need to fill in the following fields:
   - `title`: the title used in the page thumbnail.
   - `description`: the description used in the page thumbnail.
   - `url`: the URL of the notebook to render.
   - `repo_url`: the URL of the repository serving as source.
   - `image_url`: the URL of the picture to use as thumbnail.

## Deploying you own gallery

The voila gallery is built as a plugin for [The Littlest JupyterHub (TLJH)](https://tljh.jupyter.org). To deploy your own instance:

1. Fork the gallery repo: https://github.com/voila-gallery/gallery
2. Edit the `tljh-voila-gallery/tljh_voila_gallery/gallery.yaml` file with your own set of examples
3. Follow [one of the tutorials to install TLJH](https://tljh.jupyter.org/en/latest/#installation)
4. At the step asking for user data, use the following command:

```
#!/bin/bash
curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py \
 | sudo python3 - \
   --plugin git+https://github.com/<your-username>/gallery@master#"egg=tljh-voila-gallery&subdirectory=tljh-voila-gallery"
```
5. The install process might take between 5 and 10 minutes to complete.
6. Dependending on the method and cloud provider chosen in step 1, you will get the public IP of the server, which can be used to access the gallery
