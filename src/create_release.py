import logging
import coloredlogs
coloredlogs.install(level="DEBUG")
coloredlogs.auto_install()
logging.getLogger().setLevel(logging.WARNING)

from release_creator.release_creator import create_release  # noqa


if __name__ == "__main__":
    create_release()
