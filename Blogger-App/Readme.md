
py -3 -m venv venv

venv/Scripts/activate.bat

set FLASK_APP=blogs
set FLASK_ENV=development

flask init-db

flask run

