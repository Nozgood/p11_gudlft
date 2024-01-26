from datetime import datetime
import json
from flask import Flask,render_template,request,redirect,flash,url_for
import os

CLUBS_JSON = 'clubs.json'
COMPETITIONS_JSON = 'competitions.json'
MAX_POINTS_ALLOWED = 12


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except IndexError:
        flash('Unknown email address')
        return redirect(url_for('index'))
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = [competition for competition in competitions if competition['name'] == request.form['competition']][0]

    club = [club for club in clubs if club['name'] == request.form['club']][0]

    print(datetime.today() > datetime.strptime(competition["date"], '%Y-%m-%d %H:%M:%S'))

    if datetime.today() > datetime.strptime(competition["date"], '%Y-%m-%d %H:%M:%S'):
        flash("you try to book places for a past competition")
        return render_template('booking.html', club=club, competition=competition)

    club_points = club['points']
    required_places = int(request.form['places'])

    if int(club_points) < required_places:
        flash("your club does not have enough points")
        return render_template('booking.html', club=club, competition=competition)
    if int(required_places) > MAX_POINTS_ALLOWED:
        flash('you cannot book more than 12 places for your club')
        return render_template('booking.html', club=club, competition=competition)
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-required_places
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))