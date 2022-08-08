from flask import Blueprint, render_template, request, jsonify
from .models import Url
from . import db, BASE_URL
import random
import string

views = Blueprint('views', __name__)


def get_unique_short_url_id():
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    while True:
        rand_letters = random.choices(letters, k=9)
        rand_letters = "".join(rand_letters)
        existing_short_url = Url.query.filter_by(
            short_url=f"{BASE_URL}{rand_letters}").first()
        if not existing_short_url:
            return rand_letters


@views.route('/')
def home():
    urls = Url.query.all()
    return render_template('index.html', urls=urls)


@views.route('/encode', methods=['POST'])
def encode():
    received_url = request.form["inputUrl"]
    existing_url = Url.query.filter_by(full_url=received_url).first()
    if existing_url:
        return jsonify(existing_url)
    else:
        url_id = get_unique_short_url_id()
        new_url = Url(received_url, f"{BASE_URL}{url_id}")
        db.session.add(new_url)
        db.session.commit()
        return jsonify(new_url)


@views.route('/decode', methods=['POST'])
def decode():
    received_url = request.form["inputUrl"]
    existing_url = Url.query.filter_by(short_url=received_url).first()
    if existing_url:
        return jsonify(existing_url)
    else:
        return jsonify({'err': 'Url does not exist'})
