# simple-api


1) virtualenv -p python3 venv; source venv/bin/activate

2) python server/manage.py migrate

3) python server/manage.py runserver

### Docs
swagger http://127.0.0.1:8000/swagger

### Tests
* python server/manage.py test apps.users
* python server/manage.py test apps.posts