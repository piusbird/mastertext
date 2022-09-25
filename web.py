#!/usr/bin/env python3
from mastertext.webfrontend import app
from gevent import monkey
monkey.patch_all()


if __name__ == '__main__':
    app.run(debug=True)
