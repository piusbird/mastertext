#!/usr/bin/env python3
"""Flask local server"""

from gevent import monkey

monkey.patch_all()
from mastertext.webfrontend import app  # noqa

if __name__ == "__main__":
    app.run(debug=True)
