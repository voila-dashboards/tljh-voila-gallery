import socket
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
    # Since dockerspawner isn't available at import time
    from dockerspawner import DockerSpawner
    class GallerySpawner(DockerSpawner):
        def options_from_form(self, formdata):
            options = {}
            if 'example' in formdata:
                options['example'] = formdata['example'][0]
            return options

        def start(self):
            gallery = get_gallery()
            examples = gallery['examples']
            chosen_example = self.user_options['example']
            assert chosen_example in examples
            self.default_url = examples[chosen_example]['url']
            self.image = examples[chosen_example]['image']
            return super().start()

    c.JupyterHub.spawner_class = GallerySpawner
    c.JupyterHub.authenticator_class = 'tmpauthenticator.TmpAuthenticator'

    c.JupyterHub.hub_connect_ip = socket.gethostname()

    # Don't kill servers when hub restarts
    c.JupyterHub.cleanup_servers = False

    # rm containers when they stop
    c.DockerSpawner.remove = True
    # Disabled until we fix it in TmpAuthenticator
    # c.TmpAuthenticator.force_new_server = True

    c.DockerSpawner.cmd = ['jupyterhub-singleuser']

    # Override JupyterHub template
    c.JupyterHub.template_paths = [TEMPLATES_PATH]

    c.Spawner.options_form = options_form

@hookimpl
def tljh_extra_apt_packages():
    return [
        'docker.io'
    ]
