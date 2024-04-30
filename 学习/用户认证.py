from werkzeug.security import generate_password_hash,check_password_hash
pw_hash=generate_password_hash('dog')
dog=check_password_hash(pw_hash,'dog')
cat=check_password_hash(pw_hash,'cat')
print(pw_hash)
print(dog,cat)

from flask_login import LoginManager

login_manager=LoginManager(app)
