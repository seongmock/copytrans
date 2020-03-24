import PyInstaller.__main__
import sys
import os
sys.setrecursionlimit(5000)

os.environ["PYTHONOPTIMIZE"] = '1'

PyInstaller.__main__.run([
    "--log-level=WARN",
    "--onefile",
    "--windowed",
    # "--hidden-import=ssl",
    "--hidden-import=pkg_resources.py2_warn",
    '--icon=icon.ico',
    'CopyTrans.py',
])