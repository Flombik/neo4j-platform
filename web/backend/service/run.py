import argparse
import os


def main():
    # pylint: disable=import-outside-toplevel
    parser = argparse.ArgumentParser(
        description="Initialize database with core elements"
    )
    parser.add_argument("--config", type=str, required=True, help="Path to config file")
    args = parser.parse_args()

    os.environ["CONFIG_PATH"] = args.config

    from .app import create_app
    from .config import config

    app = create_app()
    app.run(
        host=config.get_host(),
        port=config.get_port(),
    )
