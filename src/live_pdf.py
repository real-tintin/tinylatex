import logging
from pathlib import Path
from typing import Callable

from flask import Flask, render_template, send_file
from waitress import serve

URL_PDF_ROOT = '/does_not_really_exist'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

cache = {}
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html', pdf_path=cache['pdf_path_url'])


@app.route("/pdf_version", methods=['GET'])
def pdf_timestamp():
    return str(cache['get_version_cb']())


@app.route(URL_PDF_ROOT + '/<string:filename>')
def send_pdf(filename):
    return send_file(cache['pdf_path_src'])


def launch(host: str, port: int, pdf_path: Path, get_version_cb: Callable):
    """
    Serves pdf at host:port and live reloads it version change.
    """
    cache['pdf_path_src'] = pdf_path
    cache['pdf_path_url'] = URL_PDF_ROOT + '/' + pdf_path.name
    cache['get_version_cb'] = get_version_cb

    serve(app, host=host, port=port)  # blocking

    logger.info("Shutting down")
