#!/usr/bin/env python3
import json
import sys
from typing import List, Any

from flask import Flask, request, jsonify, Response, abort

from kvstorage import KVStorage

_g_kvstorage: KVStorage | None = None


def is_str(value):
    #updates b so that it is a boolean that indicates whether value is a string.
    b = isinstance(value, str)
    return b


def is_list_of_string(value):
    #update b so that it is a boolean that indicates whether value is a list of strings.
    b = isinstance(value, list) and all(isinstance(v, str) for v in value)
    return b


def create_app(kv: KVStorage) -> Flask:
    app = Flask(__name__)

    @app.errorhandler(400)
    def bad_request(e):
        return Response("The request is not valid", status=400, mimetype="text/plain")

    @app.route("/keys/<path:key>", methods=["GET"])
    def get_key(key: str):
        try:
            value = kv.get(key)
            if value is None:
                return Response("", status=404)
            if not is_list_of_string(value):
                return Response("", status=400)
            return jsonify(value), 200
        except Exception:
            return Response("", status=500)

    @app.route("/keys/<path:key>", methods=["POST"])
    def post_key(key: str):
        if request.mimetype != "application/json":
            abort(400)

        try:
            payload = request.get_json(force=False, silent=False)
        except Exception:
            abort(400)

        if not isinstance(payload, dict):
            abort(400)

        req_type = payload.get("type")
        req_value = payload.get("value")

        if req_type == "PUT":
            if not is_list_of_string(req_value):
                return Response("The request value is not valid", status=400, mimetype="text/plain")
            kv.put(key, req_value)
            return ("", 204)

        elif req_type == "APPEND":
            if not is_str(req_value):
                return Response("The request value is not valid", status=400, mimetype="text/plain")
            kv.append(key, req_value)
            return ("", 204)

        else:
            return Response("The request type is not correct", status=400, mimetype="text/plain")

    @app.route("/admin/status", methods=["GET"])
    def admin_status():
        try:
            status = str(kv.getStatus())
            return Response(status, status=200, mimetype="text/plain")
        except Exception:
            return Response("", status=500)

    return app


def main():
    if len(sys.argv) < 5:
        print(f"Usage: {sys.argv[0]} http_port dump_file.bin selfHost:port partner1Host:port partner2Host:port ...")
        sys.exit(1)

    http_port = int(sys.argv[1])
    self_addr = sys.argv[2]
    partners = sys.argv[3:]

    global _g_kvstorage
    _g_kvstorage = KVStorage(self_addr, partners)

    app = create_app(_g_kvstorage)
    app.run(host="0.0.0.0", port=http_port, threaded=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exit")
