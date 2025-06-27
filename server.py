import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    """Load clubs from a JSON file."""
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    """Load competitions from a JSON file."""
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


def manage_over_competitions(competitions_list):
    """take a list of competitions and return a list of competitions that are over"""
    over_competitions_list = []

    for competition in competitions_list:
        if competition["date"] < datetime.today().strftime("%Y-%m-%d"):
            over_competitions_list.append(competition)

    return over_competitions_list

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()
over_competitions = manage_over_competitions(competitions)


@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')


@app.route('/show_summary', methods=['POST'])
def show_summary():
    """Render the summary page after enter club email."""
    email = request.form['email']
    club = [c for c in clubs if c['email'] == email]
    if club:
        club = club[0]  # Get the first matching club
        return (render_template('welcome.html', club=club, comp=competitions, over=over_competitions), 200)
    elif not email:
        flash("Please enter your email address")
        return (render_template('index.html'), 400)
    elif '@' not in email or '.' not in email.split('@')[-1]:
        flash("Please enter a valid email address")
        return (render_template('index.html'), 400)
    elif not club:
        flash("Email address not found in our records")
        return (render_template('index.html'), 400)
    else:
        flash("Something went wrong-please try again")
        return (render_template('index.html'), 500)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """Render the booking page for a specific competition and club."""
    found_club = [c for c in clubs if c['name'] == club]
    found_competition = [c for c in competitions if c['name'] == competition]
    found_competition_date = datetime.strptime(found_competition[0]['date'], "%Y-%m-%d %H:%M:%S")
    if found_club and found_competition:
        found_club = found_club[0]
        found_competition = found_competition[0]
        if found_competition_date > datetime.now():
            return render_template('booking.html', club=found_club, comp=found_competition)
        else:
            flash("Competition already passed")
            return render_template('welcome.html', club=found_club, comp=competitions, over=over_competitions)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, comp=competitions, over=over_competitions)


@app.route('/purchase_places', methods=['POST'])
def purchase_places():
    """Handle the booking of places for a competition."""
    competition = [c for c in competitions if c['name'] == request.form['competition']]
    club = [c for c in clubs if c['name'] == request.form['club']]
    places_required = int(request.form['places'])
    number_of_places = int(competition[0]['number_of_places'])
    if places_required > number_of_places:
        flash('You cannot book more places than available')
        return (render_template('booking.html', club=club[0], comp=competition[0]), 400)
    elif places_required > 12:
        flash('You cannot book more than 12 places')
        return (render_template('booking.html', club=club[0], comp=competition[0]), 400)
    elif places_required > int(club[0]['points']):
        flash('Not enough points available')
        return (render_template('booking.html', club=club[0], comp=competition[0]), 400)
    elif places_required >= 1:
        competition[0]['number_of_places'] = number_of_places - places_required
        flash('Great-booking complete!')
        return (render_template('welcome.html', club=club, comp=competitions, over=over_competitions), 200)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    """Handle user logout."""
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Uncomment/comment the lines below to run the app in debug mode or not
    app.run(debug=True)
    # app.run()
