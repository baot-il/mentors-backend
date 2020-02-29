"""
This is the file that should be pointed to by Procfile, which runs the Flask application.
"""

from views import *


if __name__ == '__main__':
    app.run()
