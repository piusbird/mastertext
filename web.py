#!/usr/bin/env python3
from gevent import monkey; monkey.patch_all()

from mastertext.webfrontend import app

if __name__ == '__main__':
    app.run(debug=True)
