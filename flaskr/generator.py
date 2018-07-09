from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_file
)
from werkzeug.exceptions import abort
from flaskr.db import get_db
from . import nmm
from googleapiclient.errors import HttpError

bp = Blueprint('generator', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        title = request.form['title']
        print("title:   " + title)
        error = None

        db = get_db()
        sheet_id = db.execute(
            'SELECT sheet_id'
            ' FROM formula d'
            ' WHERE d.title = ?',
            (title,)
        ).fetchone()
        _sheet_id = sheet_id["sheet_id"]
        print(_sheet_id)
        if _sheet_id is None:
            abort(404, "formula {0} doesn't exist.".format(id))

        try:
            nmm.make(_sheet_id)
            return send_file("static/Nutrition_Label_Output.docx", attachment_filename="Nutrition_Label.docx")
        except HttpError:
            abort(404, "sheet id is invalid".format(id))

    db = get_db()
    formulas = db.execute(
        'SELECT title, sheet_id'
        ' FROM formula f'
    ).fetchall()
    print('FORMULA::::' + str(formulas))
    return render_template('recipe-list.html', formulas=formulas)

@bp.route('/create', methods=('GET', "POST"))
def create():
    if request.method == 'POST':
        title = request.form['title']
        sheet_id = request.form['sheet_id']
        error = None

        if not title:
            error = 'Please enter product #'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            print("Creating:" + title + '|' + sheet_id)
            db.execute(
                'INSERT INTO formula (title, sheet_id)'
                ' VALUES (?, ?) ',
                (title, sheet_id)
            )
            db.commit()
            return redirect(url_for('generator.index'))
    return render_template('create.html')
