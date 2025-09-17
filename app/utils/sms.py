import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioException


def get_twilio_client():
    """Get configured Twilio client"""
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    
    if not account_sid or not auth_token:
        print("Warning: Twilio credentials not configured")
        return None
    
    return Client(account_sid, auth_token)


def send_sms(to_number, message):
    """Send SMS message via Twilio"""
    client = get_twilio_client()
    if not client:
        print(f"Would send SMS to {to_number}: {message}")
        return False
    
    try:
        from_number = os.getenv('TWILIO_PHONE_NUMBER')
        if not from_number:
            print("Warning: TWILIO_PHONE_NUMBER not configured")
            return False
        
        message = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        
        print(f"SMS sent to {to_number}: {message.sid}")
        return True
        
    except TwilioException as e:
        print(f"Failed to send SMS to {to_number}: {e}")
        return False


def send_auth_code(phone, code):
    """Send authentication code via SMS"""
    message = f"Your Eliminator verification code is: {code}\n\nThis code expires in 10 minutes."
    return send_sms(phone, message)


def send_pick_reminder(phone, player_name, week, available_teams):
    """Send weekly pick reminder"""
    team_list = ", ".join(available_teams[:8])  # Limit for SMS length
    if len(available_teams) > 8:
        team_list += f" and {len(available_teams) - 8} more"
    
    message = f"Hi {player_name}! Week {week} picks due soon.\n\nAvailable teams: {team_list}\n\nReply with your pick or visit the website."
    return send_sms(phone, message)