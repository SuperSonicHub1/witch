from functools import wraps
from typing import Optional
from flask import request, render_template


def templated(template: Optional[str] = None):
    """
    From Flask's documentation (https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/#templating-decorator):

    A common pattern invented by the TurboGears guys a while back is a
    templating decorator. The idea of that decorator is that you return a
    dictionary with the values passed to the template from the view
    function and the template is automatically rendered.
    """
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            # if no template name is provided it will use the endpoint of
            # the URL map with dots converted to slashes + '.html.jinja2'
            if template_name is None:
                template_name = request.endpoint.replace(".", "/") + ".html.jinja2"
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)

        return decorated_function

    return decorator