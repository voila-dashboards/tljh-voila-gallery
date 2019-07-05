import os
import sys
from pkg_resources import resource_stream

from tljh import systemd

GALLERY_REPO = os.environ.get('GALLERY_REPO', 'git+https://github.com/voila-gallery/gallery@master#"egg=tljh-voila-gallery&subdirectory=tljh-voila-gallery"')


def ensure_builder_units():
    gallery_builder_service = 'tljh-voila-gallery-builder.service'
    with resource_stream(__name__, f'./systemd-units/{gallery_builder_service}') as f:
        builder_unit_template = f.read().decode('utf-8')

    gallery_builder_timer = 'tljh-voila-gallery-builder.timer'
    with resource_stream(__name__, f'./systemd-units/{gallery_builder_timer}') as f:
        builder_timer_template = f.read().decode('utf-8')

    unit_params = dict(
        python_interpreter_path=sys.executable,
        gallery_repo=GALLERY_REPO,
    )

    systemd.install_unit(gallery_builder_service, builder_unit_template.format(**unit_params))
    systemd.install_unit(gallery_builder_timer, builder_timer_template.format(**unit_params))

    for unit in [gallery_builder_service, gallery_builder_timer]:
        systemd.restart_service(unit)
        systemd.enable_service(unit)

    systemd.reload_daemon()


if __name__ == '__main__':
    ensure_builder_units()
