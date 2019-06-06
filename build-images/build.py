
import os
from pathlib import Path
import subprocess
import yaml
from collections import namedtuple
import logging


logging.basicConfig(level=logging.INFO)


REPO2DOCKER = '/opt/tljh/hub/bin/repo2docker'


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
            repo_url=example_yaml['repo-url']
        )
        examples.append(example)
    return examples


def main():
    here = Path(os.path.dirname(os.path.abspath(__file__)))
    config_path = here / '../gallery.yaml'
    with config_path.open() as fp:
        examples = parse_gallery_config(fp)
    for example in examples:
        logging.info(f'Building image {example.image}')
        build_image(example)


if __name__ == '__main__':
    main()
