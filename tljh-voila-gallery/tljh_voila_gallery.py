import socket
import os
import jinja2
from ruamel.yaml import YAML
from tljh.hooks import hookimpl

yaml = YAML()

HERE = os.path.dirname(os.path.abspath(__file__))

# FIXME: Make this configurable?
GALLERY_PATH = os.path.join(HERE, '..', 'gallery.yaml')

TEMPLATES_PATH = os.path.join(HERE, 'templates')

# Read gallery.yaml on each spawn. If this gets too expensive, cache it here
def get_gallery():
    with open(GALLERY_PATH) as f:
        return yaml.load(f)


def options_form(spawner):
    # Load the files each time, so we can put them in a different
    # 'data' repository where they can be updated without requiring
    # JupyterHub restarts
    with open(GALLERY_PATH) as f:
        gallery = yaml.load(f)

    with open(os.path.join(TEMPLATES_PATH, 'options_form.html')) as f:
        return jinja2.Template(f.read()).render(images=gallery['items'])

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
            examples = gallery['example']
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
def tljh_extra_hub_pip_packages():
    return [
        'dockerspawner',
        'git+https://github.com/jupyter/repo2docker.git@f19e159dfe1006dbd82c7728e15cdd19751e8aec'
    ]

def tljh_extra_apt_packages():
    return [
        'docker.io'
    ]