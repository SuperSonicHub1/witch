from functools import wraps
from typing import Optional

from flask import request, render_template, jsonify


def templated(template: Optional[str] = None):
    """Easily return a template from a dict.
    Adapted from: https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/?highlight=decorators#templating-decorator
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                # If no template name is provided it will use the endpoint of the URL map with dots converted to slashes + '.html.jinja2'.
                template_name = request.endpoint.replace(".", "/") + ".html.jinja2"
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)

        return decorated_function

    return decorator


def jsoned():
    """Automatically JSONify a Flask endpoint."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ctx = f(*args, **kwargs)
            return jsonify(ctx)

        return decorated_function

    return decorator
