# Contributing

## Setting up a dev environment

Though voila-gallery is deployed as a [TLJH](https://tljh.jupyter.org)
plugin, you can develop it locally without needing TLJH. You just need
[docker](https://docker.com) and Python 3.6+ installed.

1. Create a virtual environment to work in, with your favorite
   Python virtual environment tool. With Python's built in `venv`
   module, you can make a virtual environment with:

   ```bash
   python3 -m venv .
   source bin/activate
   ```

2. Install development requirements

   ```bash
   pip install -r dev-requirements.txt
   ```
2. Do a dev install of the `tljh_voila_gallery` package.

   ```bash
   pip install -e tljh-voila-gallery
   ```

3. Install [configurable-http-proxy](https://github.com/jupyterhub/configurable-http-proxy).
   This is needed by JupyterHub, and you need [nodejs](https://nodejs.org/en/) / [npm](https://npmjs.com)
   to install it.

   ```bash
   npm -g install configurable-http-proxy
   ```

4. Build all the images

   ```bash
   python3 -m tljh_voila_gallery.build_images
   ```

   This requires docker be available and usable from your current
   user without root. If you need to use `sudo` before your `docker`
   calls, you should use `sudo $(which python3)` rather than just
   `python3`

5. Start JupyterHub with the testing config

   ```bash
   python3 -m jupyterhub -f jupyterhub_config.py
   ```

   This requires docker be available and usable from your current
   user without root. If you need to use `sudo` before your `docker`
   calls, you should use `sudo $(which python3)` rather than just
   `python3`

This should start a JupyterHub running at `https://localhost:8000`
with the current code. If you modify the JupyterHub config or the
service code / template, you need to restart JupyterHub to see their
effects.
