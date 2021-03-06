from fabric.operations import local
from fabric.api import cd, env, task, prefix, run
from contextlib import contextmanager

@task
def runserver():
    local('python runserver.py')

@task
def test():
    local('python flask_user/tests/run_tests.py')

@task
def coverage():
    local('coverage run --source=flask_user flask_user/tests/run_tests.py')
    local('coverage report -m')

@task
def babel():
    local('pybabel extract -F flask_user/translations/babel.cfg -c NOTE -o flask_user/translations/flask_user.pot flask_user flask_user')
    local('pybabel update -i flask_user/translations/flask_user.pot --domain=flask_user --output-dir flask_user/translations -l en')
    local('pybabel update -i flask_user/translations/flask_user.pot --domain=flask_user --output-dir flask_user/translations -l nl')
    local('pybabel compile -f --domain=flask_user --directory flask_user/translations')

@task
def babel_init():
    local('pybabel extract -F flask_user/translations/babel.cfg -c NOTE -o flask_user/translations/flask_user.pot flask_user flask_user')
    local('pybabel init -i flask_user/translations/flask_user.pot --domain=flask_user --output-dir flask_user/translations -l en')
    local('pybabel init -i flask_user/translations/flask_user.pot --domain=flask_user --output-dir flask_user/translations -l nl')
    local('pybabel compile -f --domain=flask_user --directory flask_user/translations')

@task
def docs():
    local('cp example_apps/*_app.py docs/source/includes/.')
    #local('touch docs/source/*.rst')
    local('sphinx-build -b html docs/source ../builds/flask_user/docs')
    local('cd ../builds/flask_user/docs && zip -u -r flask_user_docs *')

@task
def upload_to_pypi():
    local('python setup.py sdist upload')