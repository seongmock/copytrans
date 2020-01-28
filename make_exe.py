import PyInstaller.__main__

PyInstaller.__main__.run([
    "--onefile",
    "--windowed",
    "--hidden-import=ssl",
    'CopyTrans.py',
])