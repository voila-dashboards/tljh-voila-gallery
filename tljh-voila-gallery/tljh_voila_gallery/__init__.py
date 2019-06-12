import socket
import sys
import os
import jinja2
from pkg_resources import resource_stream, resource_filename
from ruamel.yaml import YAML
from tljh.hooks import hookimpl

yaml = YAML()

# FIXME: Make this configurable?
GALLERY_PATH = 'gallery.yaml'  # relative to package root

TEMPLATES_PATH = resource_filename(__name__, 'templates')

# Read gallery.yaml on each spawn. If this gets too expensive, cache it here
def get_gallery():
    with resource_stream(__name__, GALLERY_PATH) as f:
        return yaml.load(f)


def options_form(spawner):
    # Load the files each time, so we can put them in a different
    # 'data' repository where they can be updated without requiring
    # JupyterHub restarts
    gallery = get_gallery()

    with open(os.path.join(TEMPLATES_PATH, 'options_form.html')) as f:
        return jinja2.Template(f.read()).render(examples=gallery['examples'])

@hookimpl
def tljh_custom_jupyterhub_config(c):
    from dockerspawner import DockerSpawner
    from nullauthenticator import NullAuthenticator
    class GallerySpawner(DockerSpawner):
        # FIXME: What to do about idle culling?!
        cmd = 'jupyter-notebook'

        events = False

        def get_args(self):
            args = [
                '--ip=0.0.0.0',
                '--port=%i' % self.port,
                '--NotebookApp.base_url=%s' % self.server.base_url,
                '--NotebookApp.token=%s' % self.user_options['token'],
                '--NotebookApp.trust_xheaders=True',
            ]
            return args + self.args

        def start(self):
            if 'token' not in self.user_options:
                raise web.HTTPError(400, "token required")
            if 'image' not in self.user_options:
                raise web.HTTPError(400, "image required")
            self.image = self.user_options['image']
            return super().start()


    class GalleryAuthenticator(NullAuthenticator):
        auto_login = True

        def login_url(self, base_url):
            return '/services/gallery'

    c.JupyterHub.spawner_class = GallerySpawner
    c.JupyterHub.authenticator_class = GalleryAuthenticator

    c.JupyterHub.hub_connect_ip = socket.gethostname()

    # Don't kill servers when hub restarts
    c.JupyterHub.cleanup_servers = False

    # rm containers when they stop
    c.DockerSpawner.remove = True

    c.JupyterHub.services = [{
        'name': 'gallery',
        'admin': True,
        'url': 'http://127.0.0.1:9888',
        'command': [
            sys.executable, '-m', 'tljh_voila_gallery.gallery'
        ]
    }]

@hookimpl
def tljh_extra_apt_packages():
    return [
        'docker.io'
    ]
