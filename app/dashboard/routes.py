from flask import render_template
from . import bp

@bp.route('/')
def dashboard():
    return render_template('dashboard.html', title='Dashboard')
