from itsdangerous import URLSafeTimedSerializer
from project import app
from string import digits, ascii_uppercase
from random import sample

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def generate_confirmation_token_assessment(email,doctor_id,assessment_id):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps([email, doctor_id, assessment_id], salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=60 * 60 * 24 * 3):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    decrypted = serializer.loads(
        token,
        salt=app.config['SECURITY_PASSWORD_SALT'],
        max_age=expiration)
    return decrypted

def random_password():
    return ''.join(sample(ascii_uppercase + digits, k=8))    
