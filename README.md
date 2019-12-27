# Voilà Gallery plugin for The Littlest JupyterHub

![voila-gallery-logo](./voila-gallery.svg)

A plugin for [The Littlest JupyterHub (TLJH)](https://tljh.jupyter.org) that installs a [Voilà](https://voila-dashboards/voila) Gallery.

## Install

To deploy a new instance of the gallery as a plugin for The Littlest JupyterHub:

1. Fork the repo: https://github.com/voila-dashboards/tljh-voila-gallery
2. Edit `tljh-voila-gallery/tljh_voila_gallery/gallery.yaml` with your own set of examples
3. Follow [one of the tutorials to install TLJH](https://tljh.jupyter.org/en/latest/#installation)
4. At the step asking for user data, use the following command:

```
#!/bin/bash
curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py \
 | sudo python3 - \
   --plugin git+https://github.com/<your-username>/tljh-voila-gallery@master#"egg=tljh-voila-gallery&subdirectory=tljh-voila-gallery"
```
5. The install process might take between 5 and 10 minutes to complete.
6. Dependending on the method and cloud provider chosen in Step 1, you will get the public IP of the server, which can be used to access the gallery

## Going back to the gallery screen

You can go back to the gallery landing page using the back button of the web browser.

## Development

See [CONTRIBUTING.md](./CONTRIBUTING.md) to know how to contribute and set up a development environment.

## Related projects

There is a public gallery of Voilà examples, which can be found at [voila-gallery.org](https://voila-gallery.org). The source for this gallery is available at https://github.com/voila-gallery/voila-gallery.github.io.

## License

We use a shared copyright model that enables all contributors to maintain the
copyright on their contributions.

This software is licensed under the BSD-3-Clause license. See the
[LICENSE](LICENSE) file for details.
