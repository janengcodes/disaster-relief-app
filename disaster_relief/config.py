"""disaster_relief development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'\x88\x16\x86\x13\x01\x8f\x01\xa0U\xf4\x95R\xa2\xe8\x9a\x9cN7\
    xed[\xb4\xcd&\x85'
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
disaster_relief_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = disaster_relief_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/disaster_relief.sqlite3
DATABASE_FILENAME = disaster_relief_ROOT/'var'/'disaster_relief.sqlite3'
