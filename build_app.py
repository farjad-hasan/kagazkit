import os

import customtkinter
import PyInstaller.__main__
import tkinterdnd2

# Get paths for dependencies
ctk_path = os.path.dirname(customtkinter.__file__)
dnd_path = os.path.dirname(tkinterdnd2.__file__)

PyInstaller.__main__.run([
    'src/kagazkit/main.py',
    '--name=KagazKit',
    '--onefile',
    '--windowed',
    f'--add-data={ctk_path};customtkinter/',
    f'--add-data={dnd_path};tkinterdnd2/',
    '--hidden-import=PIL._tkinter_guess_binary',
    '--clean',
    '--noconfirm',
])