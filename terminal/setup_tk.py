'''
Created on 08.01.2013

@author: Jan
'''
from distutils.core import setup
import py2exe
import os

# Find GTK+ installation path
setup(
    name = 'handytool',
    description = 'Some handy tool',
    version = '1.0',

    windows = [
                  {
                      'script': 'PWMControlGui_Tk.py',
                      #'icon_resources': [(1, "handytool.ico")],
                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings',
                      'bundle_files':2,
                      # Optionally omit gio, gtk.keysyms, and/or rsvg if you're not using them
                      'includes': ["Tkinter"],#'cairo, pango, pangocairo, atk, gobject, gio, gtk.keysyms, rsvg',
                  }
              },
    #zipfile = None,

    #data_files=[
                   #'handytool.glade',
                   #'readme.txt',
                   # If using GTK+'s built in SVG support, uncomment these
                   #os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'gdk-pixbuf-query-loaders.exe'),
                   #os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'libxml2-2.dll'),
               #]
)