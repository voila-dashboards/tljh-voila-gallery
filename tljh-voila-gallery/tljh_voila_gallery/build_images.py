
import sys
import os
from pathlib import Path
import subprocess
from collections import namedtuple
from pkg_resources import resource_stream
import logging

from ruamel.yaml import YAML

logging.basicConfig(level=logging.INFO)

yaml = YAML()

GALLERY_PATH = 'gallery.yaml'  # Relative to module root


Example = namedtuple(
    'Example',
    [
        'image',
        'repo_url'
    ]
)


def build_image(example):
    subprocess.run([
        sys.executable,
        '-m',
        'repo2docker',
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
        'run ${NB_PYTHON_PREFIX}/bin/pip install --no-cache-dir voila==0.1.2',
        example.repo_url
    ])


def parse_gallery_config(fp):
    config = yaml.load(fp)
    examples = []
    for example_name, example_yaml in config['examples'].items():
        example = Example(
            image=f'{example_name}:latest',
            repo_url=example_yaml['repo_url']
        )
        examples.append(example)
    return examples


def main():
    with resource_stream(__name__, GALLERY_PATH) as fp:
        examples = parse_gallery_config(fp)
    for example in examples:
        logging.info(f'Building image {example.image}')
        build_image(example)


if __name__ == '__main__':
    main()
