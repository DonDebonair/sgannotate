# -*- coding: utf-8 -*-
from flask_assets import Bundle, Environment

css = Bundle(
    "libs/bootstrap/dist/css/bootstrap.css",
    "libs/x-editable/dist/bootstrap3-editable/css/bootstrap-editable.css",
    "css/style.css",
    filters=["cssrewrite", "cssmin"],
    output="public/public/css/common.css"
)

js = Bundle(
    "libs/jQuery/dist/jquery.js",
    "libs/bootstrap/dist/js/bootstrap.js",
    "libs/x-editable/dist/bootstrap3-editable/js/bootstrap-editable.js",
    "js/script.js",
    filters='rjsmin',
    output="public/public/js/common.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
