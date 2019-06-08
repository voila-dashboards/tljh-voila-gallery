
import os
from pathlib import Path
import subprocess
from collections import namedtuple
import logging

from ruamel.yaml import YAML

logging.basicConfig(level=logging.INFO)

yaml = YAML()

REPO2DOCKER = '/opt/tljh/hub/bin/repo2docker'
HERE = Path(os.path.dirname(os.path.abspath(__file__)))
GALLERY_PATH = HERE / '../../gallery.yaml'


Example = namedtuple(
    'Example',
    [
        'image',
        'repo_url'
    ]
)


def build_image(example):
    subprocess.run([
        REPO2DOCKER,
        '--ref',
        'master',
        '--user-name',
        'jovyan',
        '--user-id',
        '1000',
        '--no-run',
        '--image-name',
        example.image,
        '--appendix',
        'run ${NB_PYTHON_PREFIX}/bin/pip install --no-cache voila==0.1.0',
        example.repo_url
    ])


def parse_gallery_config(fp):
    config = yaml.load(fp)
    examples = []
    for example_yaml in config['examples'].values():
        example = Example(
            image=example_yaml['image'],
            repo_url=example_yaml['repo_url']
        )
        examples.append(example)
    return examples


def main():
    with GALLERY_PATH.open() as fp:
        examples = parse_gallery_config(fp)
    for example in examples:
        logging.info(f'Building image {example.image}')
        build_image(example)


if __name__ == '__main__':
    main()
