import json
import os.path

from flask import Flask, render_template, request, redirect, flash, url_for


CLUBS_JSON = 'clubs.json'
COMPETITIONS_JSON = 'competitions.json'


def load_clubs():
    current_path = os.path.dirname(os.path.abspath(__file__))
    print(f'current path: {current_path}')
    file_path = os.path.join(current_path, CLUBS_JSON)
    with open(file_path) as clubs_file:
        list_of_clubs = json.load(clubs_file)['clubs']
        return list_of_clubs


def load_competitions():
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_path, COMPETITIONS_JSON)
    with open(file_path) as competitions_file:
        list_of_competitions = json.load(competitions_file)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'
competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    if email == "":
        flash('Please fill an email')
        return redirect(url_for('index'))
    logged_club = [club for club in clubs if club['email'] == email]
    if len(logged_club) == 0:
        flash('Unknown email')
        return redirect(url_for('index'))
    return show_summary(logged_club[0])


@app.route('/showSummary')
def show_summary(logged_club):
    return render_template('welcome.html', club=logged_club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        return render_template('booking.html',club=found_club,competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    required_places = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-required_places
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
