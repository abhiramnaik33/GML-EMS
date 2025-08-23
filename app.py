from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import pandas as pd
from io import BytesIO
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///league.db'
app.config['UPLOAD_FOLDER'] = 'static/player_photos'
app.config['TEAM_LOGO_FOLDER'] = 'static/team_logos'
app.config['OWNER_PHOTO_FOLDER'] = 'static/owner_photos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sport = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(50))
    usn = db.Column(db.String(20))
    college_name = db.Column(db.String(100))
    position = db.Column(db.String(50))
    contact = db.Column(db.String(20))
    photo = db.Column(db.String(200))
    achievements = db.Column(db.Text)
    experience = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    sold = db.Column(db.Boolean, default=False)
    bid_amount = db.Column(db.Integer)
    sold_to = db.Column(db.String(100))

class TeamOwner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team_name = db.Column(db.String(100), nullable=False, unique=True)
    sports = db.Column(db.String(200), nullable=False)
    budget = db.Column(db.Integer, default=1000000)
    contact = db.Column(db.String(20))
    team_logo = db.Column(db.String(200))
    designation = db.Column(db.String(100))
    email = db.Column(db.String(100))
    manager_name = db.Column(db.String(100))
    manager_contact_number = db.Column(db.String(20))
    team_owner_photo = db.Column(db.String(200))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_player/<sport>', methods=['GET', 'POST'])
def register_player(sport):
    sport = sport.capitalize()
    if sport not in ['Football', 'Kabaddi', 'Basketball', 'Badminton']:
        flash('Invalid sport!', 'error')
        return redirect(url_for('index'))
    positions = {
        'Football': ['Goalkeeper', 'Defender', 'Midfielder', 'Forward'],
        'Kabaddi': ['Raider', 'Defender', 'All-Rounder'],
        'Basketball': ['Point Guard', 'Shooting Guard', 'Small Forward', 'Power Forward', 'Center'],
        'Badminton': ['Singles', 'Doubles']
    }
    if request.method == 'POST':
        name = request.form['name']
        branch = request.form['branch']
        usn = request.form['usn']
        college_name = request.form['college_name']
        position = request.form['position']
        contact = request.form['contact']
        achievements = request.form['achievements']
        experience = request.form['experience']
        gender = request.form['gender']
        photo = request.files.get('photo')
        photo_filename = None
        if photo and allowed_file(photo.filename):
            photo_filename = secure_filename(f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{photo.filename}")
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
            photo_filename = f"player_photos/{photo_filename}"
        player = Player(
            name=name, sport=sport, branch=branch, usn=usn, college_name=college_name,
            position=position, contact=contact, photo=photo_filename, achievements=achievements,
            experience=experience, gender=gender
        )
        try:
            db.session.add(player)
            db.session.commit()
            flash('Player registered successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error registering player: {str(e)}', 'error')
        return redirect(url_for('index'))
    return render_template('register_player.html', sport=sport, positions=positions[sport])

@app.route('/team_owner_registration', methods=['GET', 'POST'])
def team_owner_registration():
    if request.method == 'POST':
        name = request.form['name']
        team_name = request.form['team_name']
        contact = request.form['contact']
        designation = request.form['designation']
        email = request.form['email']
        manager_name = request.form['manager_name']
        manager_contact_number = request.form['manager_contact_number']
        sports_list = request.form.getlist('sports')
        if not sports_list:
            flash('At least one sport must be selected!', 'error')
            return redirect(url_for('team_owner_registration'))
        sports = ','.join([sport.split('(')[0].strip() for sport in sports_list])
        team_logo = request.files.get('team_logo')
        team_owner_photo = request.files.get('team_owner_photo')
        logo_filename = None
        photo_filename = None
        if team_logo and allowed_file(team_logo.filename):
            logo_filename = secure_filename(f"{team_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{team_logo.filename}")
            team_logo.save(os.path.join(app.config['TEAM_LOGO_FOLDER'], logo_filename))
            logo_filename = f"team_logos/{logo_filename}"
        if team_owner_photo and allowed_file(team_owner_photo.filename):
            photo_filename = secure_filename(f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{team_owner_photo.filename}")
            team_owner_photo.save(os.path.join(app.config['OWNER_PHOTO_FOLDER'], photo_filename))
            photo_filename = f"owner_photos/{photo_filename}"
        owner = TeamOwner(
            name=name, team_name=team_name, sports=sports, contact=contact,
            team_logo=logo_filename, designation=designation, email=email,
            manager_name=manager_name, manager_contact_number=manager_contact_number,
            team_owner_photo=photo_filename
        )
        try:
            db.session.add(owner)
            db.session.commit()
            flash('Team owner registered successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error registering team owner: {str(e)}', 'error')
            return redirect(url_for('team_owner_registration'))
    sports = [
        'Football(Men)', 'Basketball(Men)', 'Basketball(Women)', 
        'Kabaddi(Men)', 'Kabaddi(Women)', 'Badminton(Men)', 'Badminton(Women)'
    ]
    return render_template('team_owner_registration.html', sports=sports)

@app.route('/bidding/<sport>/<gender>', methods=['GET', 'POST'])
def bidding(sport, gender):
    sport = sport.capitalize()
    gender = gender.capitalize()
    if sport not in ['Football', 'Kabaddi', 'Basketball', 'Badminton']:
        flash('Invalid sport!', 'error')
        return redirect(url_for('index'))
    if gender not in ['Male', 'Female'] or (sport == 'Football' and gender == 'Female'):
        flash('Invalid gender or sport combination!', 'error')
        return redirect(url_for('index'))
    if sport == 'Football':
        players = Player.query.filter_by(sport=sport, gender='Male', sold=False).all()
    else:
        players = Player.query.filter_by(sport=sport, gender=gender, sold=False).all()
    owners = TeamOwner.query.filter(TeamOwner.sports.ilike(f'%{sport}%')).all()
    if not players:
        flash(f'No unsold {gender.lower()} players available for {sport}!', 'info')
    if request.method == 'POST':
        player_id = request.form['player_id']
        owner_id = request.form['owner_id']
        bid_amount = request.form['bid_amount']
        player = Player.query.get(player_id)
        owner = TeamOwner.query.get(owner_id)
        if player and owner:
            try:
                bid_amount = int(bid_amount)
                if bid_amount <= 0:
                    flash('Bid amount must be positive!', 'error')
                elif bid_amount > owner.budget:
                    flash('Bid amount exceeds owner budget!', 'error')
                else:
                    player.sold = True
                    player.bid_amount = bid_amount
                    player.sold_to = owner.team_name
                    owner.budget -= bid_amount
                    db.session.commit()
                    flash(f'Bid successful for player {player.name} by team {owner.team_name} for {bid_amount}', 'success')
            except ValueError:
                flash('Invalid bid amount!', 'error')
        else:
            flash('Invalid player or owner selected.', 'error')
        return redirect(url_for('bidding', sport=sport.lower(), gender=gender.lower()))
    return render_template('bidding.html', sport=sport, gender=gender, players=players, owners=owners)

@app.route('/terms')
def terms():
    return render_template('terms.html')

# Admin Routes
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials!', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in', False):
        flash('Admin login required!', 'error')
        return redirect(url_for('admin_login'))
    football_players = Player.query.filter_by(sport='Football').all()
    kabaddi_players = Player.query.filter_by(sport='Kabaddi').all()
    basketball_players = Player.query.filter_by(sport='Basketball').all()
    badminton_players = Player.query.filter_by(sport='Badminton').all()
    owners = TeamOwner.query.all()
    sold_players = Player.query.filter_by(sold=True).all()
    return render_template('admin_dashboard.html', football_players=football_players, kabaddi_players=kabaddi_players,
                           basketball_players=basketball_players, badminton_players=badminton_players,
                           owners=owners, sold_players=sold_players)

@app.route('/admin/reset_bid/<int:player_id>', methods=['POST'])
def admin_reset_bid(player_id):
    if not session.get('admin_logged_in', False):
        flash('Admin login required!', 'error')
        return redirect(url_for('admin_login'))
    player = Player.query.get_or_404(player_id)
    owner = TeamOwner.query.filter_by(team_name=player.sold_to).first()
    if owner and player.bid_amount:
        owner.budget += player.bid_amount
    player.sold = False
    player.bid_amount = None
    player.sold_to = None
    try:
        db.session.commit()
        flash(f'Bid reset for player {player.name}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error resetting bid: {str(e)}', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_player/<int:id>', methods=['POST'])
def admin_delete_player(id):
    if not session.get('admin_logged_in', False):
        flash('Admin login required!', 'error')
        return redirect(url_for('admin_login'))
    player = Player.query.get_or_404(id)
    try:
        if player.photo and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(player.photo))):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(player.photo)))
        db.session.delete(player)
        db.session.commit()
        flash(f'Player {player.name} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting player: {str(e)}', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_owner/<int:id>', methods=['POST'])
def admin_delete_owner(id):
    if not session.get('admin_logged_in', False):
        flash('Admin login required!', 'error')
        return redirect(url_for('admin_login'))
    owner = TeamOwner.query.get_or_404(id)
    try:
        if owner.team_logo and os.path.exists(os.path.join(app.config['TEAM_LOGO_FOLDER'], os.path.basename(owner.team_logo))):
            os.remove(os.path.join(app.config['TEAM_LOGO_FOLDER'], os.path.basename(owner.team_logo)))
        if owner.team_owner_photo and os.path.exists(os.path.join(app.config['OWNER_PHOTO_FOLDER'], os.path.basename(owner.team_owner_photo))):
            os.remove(os.path.join(app.config['OWNER_PHOTO_FOLDER'], os.path.basename(owner.team_owner_photo)))
        db.session.delete(owner)
        db.session.commit()
        flash(f'Team owner {owner.team_name} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting team owner: {str(e)}', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_players', methods=['POST'])
def admin_delete_players():
    if not session.get('admin_logged_in', False):
        flash('Admin login required!', 'error')
        return redirect(url_for('admin_login'))
    data = request.get_json()
    ids = data.get('ids', [])
    if not ids:
        return json.dumps({'error': 'No players selected'}), 400
    try:
        for id in ids:
            player = Player.query.get(id)
            if player:
                if player.photo and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(player.photo))):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(player.photo)))
                db.session.delete(player)
        db.session.commit()
        return json.dumps({'message': 'Players deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return json.dumps({'error': f'Error deleting players: {str(e)}'}), 500

@app.route('/admin/delete_owners', methods=['POST'])
def admin_delete_owners():
    if not session.get('admin_logged_in', False):
        flash('Admin login required!', 'error')
        return redirect(url_for('admin_login'))
    data = request.get_json()
    ids = data.get('ids', [])
    if not ids:
        return json.dumps({'error': 'No owners selected'}), 400
    try:
        for id in ids:
            owner = TeamOwner.query.get(id)
            if owner:
                if owner.team_logo and os.path.exists(os.path.join(app.config['TEAM_LOGO_FOLDER'], os.path.basename(owner.team_logo))):
                    os.remove(os.path.join(app.config['TEAM_LOGO_FOLDER'], os.path.basename(owner.team_logo)))
                if owner.team_owner_photo and os.path.exists(os.path.join(app.config['OWNER_PHOTO_FOLDER'], os.path.basename(owner.team_owner_photo))):
                    os.remove(os.path.join(app.config['OWNER_PHOTO_FOLDER'], os.path.basename(owner.team_owner_photo)))
                db.session.delete(owner)
        db.session.commit()
        return json.dumps({'message': 'Owners deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return json.dumps({'error': f'Error deleting owners: {str(e)}'}), 500

@app.route('/admin/edit_player/<int:id>', methods=['GET', 'POST'])
def admin_edit_player(id):
    if not session.get('admin_logged_in', False):
        flash('Admin login required!', 'error')
        return redirect(url_for('admin_login'))
    player = Player.query.get_or_404(id)
    positions = {
        'Football': ['Goalkeeper', 'Defender', 'Midfielder', 'Forward'],
        'Kabaddi': ['Raider', 'Defender', 'All-Rounder'],
        'Basketball': ['Point Guard', 'Shooting Guard', 'Small Forward', 'Power Forward', 'Center'],
        'Badminton': ['Singles', 'Doubles']
    }
    if request.method == 'POST':
        try:
            player.name = request.form['name']
            player.sport = request.form['sport']
            player.position = request.form['position'] if player.sport != 'Badminton' else None
            player.branch = request.form['branch'] or None
            player.usn = request.form['usn'] or None
            player.college_name = request.form['college_name'] or None
            player.contact = request.form['contact'] or None
            player.achievements = request.form['achievements'] or None
            player.experience = request.form['experience']
            player.gender = request.form['gender']
            photo = request.files.get('photo')
            if photo and allowed_file(photo.filename):
                if player.photo and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(player.photo))):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(player.photo)))
                photo_filename = secure_filename(f"{player.name}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{photo.filename}")
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
                player.photo = f"player_photos/{photo_filename}"
            db.session.commit()
            flash(f'Player {player.name} updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating player: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_player.html', player=player, positions=positions.get(player.sport, []))

@app.route('/admin/edit_team_owner/<int:id>', methods=['GET', 'POST'])
def admin_edit_team_owner(id):
    if not session.get('admin_logged_in', False):
        flash('Admin login required!', 'error')
        return redirect(url_for('admin_login'))
    owner = TeamOwner.query.get_or_404(id)
    sports = ['Football(Men)', 'Basketball(Men)', 'Basketball(Women)', 'Kabaddi(Men)', 'Kabaddi(Women)', 'Badminton(Men)', 'Badminton(Women)']
    if request.method == 'POST':
        try:
            owner.name = request.form['name']
            owner.team_name = request.form['team_name']
            sports_list = request.form.getlist('sports')
            if not sports_list:
                flash('At least one sport must be selected!', 'error')
                return redirect(url_for('admin_dashboard'))
            owner.sports = ','.join(sports_list)
            owner.budget = int(request.form['budget'])
            owner.contact = request.form['contact'] or None
            owner.designation = request.form['designation'] or None
            owner.email = request.form['email'] or None
            owner.manager_name = request.form['manager_name'] or None
            owner.manager_contact_number = request.form['manager_contact_number'] or None
            team_logo = request.files.get('team_logo')
            if team_logo and allowed_file(team_logo.filename):
                if owner.team_logo and os.path.exists(os.path.join(app.config['TEAM_LOGO_FOLDER'], os.path.basename(owner.team_logo))):
                    os.remove(os.path.join(app.config['TEAM_LOGO_FOLDER'], os.path.basename(owner.team_logo)))
                logo_filename = secure_filename(f"{owner.team_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{team_logo.filename}")
                team_logo.save(os.path.join(app.config['TEAM_LOGO_FOLDER'], logo_filename))
                owner.team_logo = f"team_logos/{logo_filename}"
            team_owner_photo = request.files.get('team_owner_photo')
            if team_owner_photo and allowed_file(team_owner_photo.filename):
                if owner.team_owner_photo and os.path.exists(os.path.join(app.config['OWNER_PHOTO_FOLDER'], os.path.basename(owner.team_owner_photo))):
                    os.remove(os.path.join(app.config['OWNER_PHOTO_FOLDER'], os.path.basename(owner.team_owner_photo)))
                photo_filename = secure_filename(f"{owner.name}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{team_owner_photo.filename}")
                team_owner_photo.save(os.path.join(app.config['OWNER_PHOTO_FOLDER'], photo_filename))
                owner.team_owner_photo = f"owner_photos/{photo_filename}"
            db.session.commit()
            flash(f'Team owner {owner.team_name} updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating team owner: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_team_owner.html', owner=owner, sports=sports)

@app.route('/export_summary/<sport>')
def export_summary(sport):
    if not session.get('admin_logged_in', False):
        flash('Admin login required!', 'error')
        return redirect(url_for('admin_dashboard'))
    sport = sport.capitalize()
    if sport not in ['Football', 'Kabaddi', 'Basketball', 'Badminton']:
        flash('Invalid sport!', 'error')
        return redirect(url_for('admin_dashboard'))
    players = Player.query.filter_by(sport=sport).all()
    data = [{
        'Name': p.name,
        'Branch': p.branch or 'N/A',
        'USN': p.usn or 'N/A',
        'College': p.college_name or 'N/A',
        'Position': p.position or 'N/A' if sport != 'Badminton' else 'N/A',
        'Contact': p.contact or 'N/A',
        'Gender': p.gender or 'N/A',
        'Experience': p.experience or 'N/A',
        'Achievements': p.achievements or 'None',
        'Sold To': p.sold_to or 'Not Sold',
        'Bid Amount': p.bid_amount or 'N/A',
        'Photo': p.photo or 'N/A'
    } for p in players]
    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_excel(output, index=False, engine='xlsxwriter')
    output.seek(0)
    return send_file(output, download_name=f"{sport}_Players.xlsx", as_attachment=True)

@app.route('/export_all_summaries')
def export_all_summaries():
    if not session.get('admin_logged_in', False):
        flash('Admin login required!', 'error')
        return redirect(url_for('admin_dashboard'))
    sports = ['Football', 'Kabaddi', 'Basketball', 'Badminton']
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sport in sports:
            players = Player.query.filter_by(sport=sport).all()
            data = [{
                'Name': p.name,
                'Branch': p.branch or 'N/A',
                'USN': p.usn or 'N/A',
                'College': p.college_name or 'N/A',
                'Position': p.position or 'N/A' if sport != 'Badminton' else 'N/A',
                'Contact': p.contact or 'N/A',
                'Gender': p.gender or 'N/A',
                'Experience': p.experience or 'N/A',
                'Achievements': p.achievements or 'None',
                'Sold To': p.sold_to or 'Not Sold',
                'Bid Amount': p.bid_amount or 'N/A',
                'Photo': p.photo or 'N/A'
            } for p in players]
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=sport, index=False)
    output.seek(0)
    return send_file(output, download_name="All_Sports_Summary.xlsx", as_attachment=True)

@app.route('/export_owners')
def export_owners():
    if not session.get('admin_logged_in', False):
        flash('Admin login required!', 'error')
        return redirect(url_for('admin_dashboard'))
    owners = TeamOwner.query.all()
    data = [{
        'Team Name': owner.team_name,
        'Owner': owner.name,
        'Budget': owner.budget,
        'Sports': owner.sports,
        'Contact': owner.contact or 'N/A',
        'Designation': owner.designation or 'N/A',
        'Email': owner.email or 'N/A',
        'Manager Name': owner.manager_name or 'N/A',
        'Manager Contact': owner.manager_contact_number or 'N/A'
    } for owner in owners]
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Team Owners')
    output.seek(0)
    return send_file(output, download_name="Team_Owners.xlsx", as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)