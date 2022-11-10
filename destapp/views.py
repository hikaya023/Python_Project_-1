from flask import Blueprint, url_for, jsonify
from flask_login import login_user, login_required, current_user

from destapp.models import Note, Item
from . import db
from flask import flash,request,redirect,send_file,render_template
from io import BytesIO
import json

import stripe


ALLOWED_EXTENSION = {'txt', 'pdf', 'jpg', 'jpeg', 'png','gif', 'jfif', 'docx', 'pptx'}
views = Blueprint('views', __name__, template_folder='templates')

def allowed_files(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@views.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)

@views.route('/api')
def api():
    return render_template('api.html', user=current_user)

@views.route('/about')
@login_required
def about():
    return render_template('about.html', user=current_user)


@views.route('/contact')
@login_required
def contact():
    return render_template('contacts.html', user=current_user)


@views.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files.get('file')

        if file.filename == '':
            flash('No file was selected')
            return redirect(request.url)

        if file and allowed_files(file.filename):
            new_file = Item(name=file.filename, data = file.read(), user_id=current_user.id)
            db.session.add(new_file)
            db.session.commit()
            flash('File uploaded successfully')
            return redirect(url_for('views.index'))

    return render_template('upload.html', user=current_user)

@views.route("/files", methods=["GET"])
def files():
    see_items = Item().query.all()
    return render_template('files.html', items=see_items, user=current_user)

@views.route("/download/<int:id>", methods=["GET"])
def download(id):
    item = Item().query.filter_by(id=id).first()
    return send_file(BytesIO(item.data), mimetype='image.png', as_attachment=True, download_name=item.name)

@views.route("/result", methods=["GET", "POST"])
def result():
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        country = request.form.get('country')
        donation = request.form.get('donation')
        prefix = request.form.get('prefix')
        pet = request.form.get('pet')

        new_resume = Note(f_name=f_name, country=country, donation=donation, prefix=prefix,
                          pet=pet, user_id=current_user.id)
        db.session.add(new_resume)
        db.session.commit()

    return render_template('see_resume.html', user=current_user)

@views.route('/resume', methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        country = request.form.get('country')
        donation = request.form.get('donation')
        prefix = request.form.get('prefix')
        pet = request.form.get('pet')


        if len(f_name) < 2:
            flash('Nickname must be greater than 1 character.', category='error')
        elif len(country) < 2:
            flash('Country name must be greater than 1 character.', category='error')
        elif len(donation) < 4:
            flash('Privilege of player must be greater than 3 characters.', category='error')
        elif len(prefix) < 2:
            flash('Prefix type is incorrect', category='error')
        elif len(pet) < 1:
            flash('The pet must be greater than 1 character.', category='error')
        else:
            new_resume = Note(f_name=f_name, country=country, donation=donation, prefix=prefix,
                              pet=pet, user_id=current_user.id)
            db.session.add(new_resume)
            db.session.commit()
            # login_user(new_resume, remember=True)
            return redirect(url_for('views.result'))
    return render_template('note.html', user=current_user)


@views.route('/delete_resume', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


@views.route('/delete_item', methods=['POST'])
def delete_item():
    item = json.loads(request.data)
    itemId = item['itemId']
    item = Item.query.get(itemId)
    if item:
        if item.user_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
    return jsonify({})

YOUR_DOMAIN = "http://127.0.0.1:3333"
stripe.api_key = "sk_test_51M2KJBG4gjimdsyeqnlTloqXaHMDgmc6dYWkF4N005kKw5gFql4ygn3mJd2MhJCY2IvTIvHs1GcWtfXSukM1fNyO00TxVT8luW "
@views.route('/buy', methods=['GET'])
@login_required
def buy():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price':'price_1M2KtFG4gjimdsyeGlhmwusp',
                    'quantity': 1
                }
            ],
            mode="subscription",
            success_url=YOUR_DOMAIN + "/success",
            cancel_url = YOUR_DOMAIN + "/cancel"
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@views.route('/success')
@login_required
def success():
    item = 'static/images/meme.jpg'
    return send_file(item, mimetype='image.png', as_attachment=True, download_name=item)


