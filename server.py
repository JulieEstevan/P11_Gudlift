import json
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


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


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
        return render_template('welcome.html', club=club, comp=competitions)
    elif not email:
        flash("Please enter your email address")
        return render_template('index.html')
    elif '@' not in email or '.' not in email.split('@')[-1]:
        flash("Please enter a valid email address")
        return render_template('index.html')
    elif not club:
        flash("Email address not found in our records")
        return render_template('index.html')
    else:
        flash("Something went wrong-please try again")
        return render_template('index.html')
    


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """Render the booking page for a specific competition and club."""
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchase_places', methods=['POST'])
def purchase_places():
    """Handle the booking of places for a competition."""
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    competition['number_of_places'] = int(competition['number_of_places']) - places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    """Handle user logout."""
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Uncomment/comment the lines below to run the app in debug mode or not
    app.run(debug=True)
    # app.run()
