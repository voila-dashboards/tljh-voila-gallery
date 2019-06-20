import socket
import sys
import os
import jinja2
from pkg_resources import resource_stream, resource_filename
from ruamel.yaml import YAML
from tljh.hooks import hookimpl
from tornado import web, gen

from dockerspawner import DockerSpawner
from tmpauthenticator import TmpAuthenticator


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

class GallerySpawner(DockerSpawner):
    # FIXME: cmd should be picked up without manually setting `_user_set_cmd`
    _user_set_cmd = True
    cmd = ['jupyterhub-singleuser']
    network_name = "host"
    events = False

    def get_args(self):
        args = [
            '--ip=0.0.0.0',
            '--port=%i' % self.port,
        ]
        return args + self.args

    @gen.coroutine
    def get_ip_and_port(self):
        return self.host_ip, self.port

    def start(self):
        if 'token' not in self.user_options:
            raise web.HTTPError(400, "token required")
        if 'image' not in self.user_options:
            raise web.HTTPError(400, "image required")
        self.image = self.user_options['image']
        return super().start()


class GalleryAuthenticator(TmpAuthenticator):
    auto_login = True

    def login_url(self, base_url):
        return '/services/gallery'

@hookimpl
def tljh_custom_jupyterhub_config(c):

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
