from flask import render_template, abort, redirect, url_for, flash, request, current_app, jsonify
from app.odontograma import bp

@bp.route('/')
def index():
    return render_template('odontograma/index.html')