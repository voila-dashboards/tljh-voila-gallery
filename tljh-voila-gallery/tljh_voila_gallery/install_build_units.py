import sys
from pkg_resources import resource_stream

from tljh import systemd

def main():
    gallery_builder_service = 'tljh-voila-gallery-builder.service'
    with resource_stream(__name__, f'./systemd-units/{gallery_builder_service}') as f:
        builder_unit_template = f.read().decode('utf-8')

    gallery_builder_timer = 'tljh-voila-gallery-builder.timer'
    with resource_stream(__name__, f'./systemd-units/{gallery_builder_timer}') as f:
        builder_timer_template = f.read().decode('utf-8')

    unit_params = dict(
        python_interpreter_path=sys.executable,
    )

    systemd.install_unit(gallery_builder_service, builder_unit_template.format(**unit_params))
    systemd.install_unit(gallery_builder_timer, builder_timer_template.format(**unit_params))

    for unit in [gallery_builder_service, gallery_builder_timer]:
        systemd.restart_service(unit)
        systemd.enable_service(unit)

    systemd.reload_daemon()


if __name__ == '__main__':
    main()
