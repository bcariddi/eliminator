import random
import string
from datetime import datetime, timedelta
from flask import render_template, request, session, redirect, url_for, flash
from app.auth import bp
from app.models import Player, AuthCode
from app import db
from app.utils.sms import send_auth_code


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Phone-based login - step 1: enter phone number"""
    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        
        # Basic phone validation
        if not phone:
            flash('Please enter a phone number')
            return render_template('auth/login.html')
        
        # Normalize phone number (remove non-digits, add +1 if needed)
        phone_digits = ''.join(filter(str.isdigit, phone))
        if len(phone_digits) == 10:
            phone = f'+1{phone_digits}'
        elif len(phone_digits) == 11 and phone_digits.startswith('1'):
            phone = f'+{phone_digits}'
        else:
            flash('Please enter a valid US phone number')
            return render_template('auth/login.html')
        
        # Generate 6-digit code
        code = ''.join(random.choices(string.digits, k=6))
        
        # Save code to database (expires in 10 minutes)
        auth_code = AuthCode(
            phone=phone,
            code=code,
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        db.session.add(auth_code)
        db.session.commit()
        
        # Send SMS with code
        if send_auth_code(phone, code):
            session['auth_phone'] = phone
            return redirect(url_for('auth.verify'))
        else:
            flash('Failed to send verification code. Please try again.')
    
    return render_template('auth/login.html')


@bp.route('/verify', methods=['GET', 'POST'])
def verify():
    """Verify SMS code - step 2"""
    if 'auth_phone' not in session:
        return redirect(url_for('auth.login'))
    
    phone = session['auth_phone']
    
    if request.method == 'POST':
        entered_code = request.form.get('code', '').strip()
        
        # Find valid, unused code
        auth_code = AuthCode.query.filter_by(
            phone=phone,
            code=entered_code,
            used=False
        ).filter(AuthCode.expires_at > datetime.utcnow()).first()
        
        if auth_code:
            # Mark code as used
            auth_code.used = True
            db.session.commit()
            
            # Check if player exists
            player = Player.query.filter_by(phone=phone).first()
            if not player:
                # New player - redirect to registration
                return redirect(url_for('auth.register'))
            else:
                # Login existing player
                session['player_id'] = player.id
                session.pop('auth_phone', None)
                flash(f'Welcome back, {player.name}!')
                return redirect(url_for('main.index'))
        else:
            flash('Invalid or expired code. Please try again.')
    
    return render_template('auth/verify.html', phone=phone)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register new player after SMS verification"""
    if 'auth_phone' not in session:
        return redirect(url_for('auth.login'))
    
    phone = session['auth_phone']
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        
        if not name:
            flash('Please enter your name')
            return render_template('auth/register.html', phone=phone)
        
        # Create new player
        player = Player(phone=phone, name=name)
        db.session.add(player)
        db.session.commit()
        
        # Login the new player
        session['player_id'] = player.id
        session.pop('auth_phone', None)
        
        flash(f'Welcome to Eliminator, {player.name}!')
        return redirect(url_for('main.index'))
    
    return render_template('auth/register.html', phone=phone)


@bp.route('/logout')
def logout():
    """Logout - clear session"""
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('main.index'))