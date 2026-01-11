from flask import render_template


def unauthorized(e):
    kwargs = {
        "error_name": "401 Unauthorized",
        "error_description": "Debe iniciar sesión para acceder al recurso",
    }
    return render_template("error401.html", **kwargs), 401
    
