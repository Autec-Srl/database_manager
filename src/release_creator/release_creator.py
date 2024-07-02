from datetime import datetime
import traceback
import PyInstaller.__main__
import logging
import coloredlogs
import os
import shutil
from pathlib import Path
import pathlib
import subprocess

# import tkinter as tk
# from tkinter import messagebox
import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

# sets logger
coloredlogs.auto_install()
logger = logging.getLogger("release_creator")
logger.setLevel(logging.INFO)


def splash_manager():
    """
    Sets the executible's splash screen and manages eventual errors when
    importing and utilizing pyi_splash module from PyInstaller.

    """
    try:
        import pyi_splash  # type: ignore
        pyi_splash.close()
    except Exception as er:
        logger.debug(f"{type(er).__name__}: splash screen was skipped as "
                     "'pyi_splash' module couldn't be loaded from PyInstaller")


def create_release(app_name: str = None):
    '''
    Create a release based on project
    '''

    # Folder naming and cleaning-up
    main_path = Path(os.path.dirname(__file__)).parent.resolve()
    if app_name is None:
        app_name = (str(main_path.parent.name)).lower()
    dist_path = main_path.joinpath("dist")
    build_path = main_path.joinpath("build")

    if os.path.exists(dist_path):
        shutil.rmtree(dist_path)

    if os.path.exists(build_path):
        shutil.rmtree(build_path)

    logger.info(f"Started the generation of '{app_name}.exe' file, please "
                "wait...")

    # Get current version info
    # Insert here additional check on versioning
    # Still not managed! a Version Manager should be appliedile()
    
    # Start a 
    start_dt = datetime.now()

    try:
        # call pyinstaller directly
        PyInstaller.__main__.run(
            [fr"{main_path}/main.py",
             '-n', app_name,
             '--log-level', 'DEBUG',
             '--clean',
             '--noconfirm',
             '--console',
             '--onefile',
             '--icon', str(main_path.joinpath("res").joinpath("ico.ico")),
             #  '--splash', str(fr"{main_path}/res/SPLASH.jpg"),
             '--add-data', str(fr"{main_path}/res;res"),
             '--specpath', str(dist_path),
             '--distpath', str(dist_path),
             '--workpath', str(build_path),
             ])
    except Exception as e:
        shutil.rmtree(build_path)
        shutil.rmtree(dist_path)
        logger.error("Release generation failed. Got exception:\n"
                     f"{traceback.format_exc()}\n"
                     f"{type(e)}: {e}")
    else:
        end_dt = datetime.now()
        td = end_dt - start_dt
        shutil.rmtree(build_path)
        logger.info(f"Release generation took {td.seconds // 60} min and "
                    f"{td.seconds % 60} s.")
        logger.info(f"Release available in '{dist_path}'")
        subprocess.Popen(f'explorer {dist_path}')
