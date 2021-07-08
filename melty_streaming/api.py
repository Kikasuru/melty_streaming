import os
import json
import flask

from proc import ProcessHook

MELTY_HEADER = 0x400000

def create_app():
    """Creates the Flask app"""
    local_dir = os.path.dirname(os.path.realpath(__file__))
    app = flask.Flask(__name__)

    @app.route("/", defaults={"req_path": "index.html"})
    @app.route("/<path:req_path>")
    def get_file(req_path):
        file_path = os.path.join(local_dir, "static", req_path)

        # Return 404 if this file doesn't exist
        if not os.path.isfile(file_path):
            return flask.abort(404)

        # Otherwise, send the file
        return flask.send_file(file_path)

    @app.route("/state")
    def get_state():
        # If the header for Melty does not exist, try to find Melty Blood.
        if ProcessHook.read(MELTY_HEADER) is None:
            # If melty is not found, return a waiting for melty statement
            if ProcessHook.look_for_melty() is False:
                return json.dumps({"waiting": True})

        state_info = {
            "waiting": False,
            "gamemode": ProcessHook.read(0x54EEE8),

            "p1selmode": ProcessHook.read(0x74D8EC),
            "p1char": ProcessHook.read(0x74D8FC),
            "p1moon": ProcessHook.read(0x74D900),
            "p1color": ProcessHook.read(0x74D904),
            "p1heat": ProcessHook.read(0x555218),

            "p2selmode": ProcessHook.read(0x74D910),
            "p2char": ProcessHook.read(0x74D920),
            "p2moon": ProcessHook.read(0x74D924),
            "p2color": ProcessHook.read(0x74D928),
            "p2heat": ProcessHook.read(0x555D14)
        }
        return json.dumps(state_info)

    return app
