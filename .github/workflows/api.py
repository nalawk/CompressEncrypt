import flask
from flask import request, jsonify
import CompressEncrypt
import timeit
import threading
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Compress & Encrypt</h1><p>A prototype API for data compression & encryption.</p>"

@app.route('/fetch', methods=['GET'])
def api_size():
    # Check if a size was provided as part of the URL.
    # If size is provided, assign it to a variable.
    # If no size is provided, display an error in the browser.
    print("PID = ", os.getpid())
    if 'size' in request.args:
        size = int(request.args['size'])

        outer_start_time = timeit.timeit()
        # cProfile.run('main()')
        threads = []

        data_block = CompressEncrypt.return_compressed_encrypted_data(size, CompressEncrypt.generate_return_key())

        outer_end_time = timeit.timeit()
        print("Total outer execution time : ", outer_end_time - outer_start_time)

        return jsonify(data_block=str(data_block))
    else:
        return "Error: No size field provided. Please specify number of bytes."


app.run()