import os
import unittest

from flask_migrate import Migrate, MigrateCommand, upgrade


from app import create_app, db


app = create_app(os.getenv('FLASK_ENV') or 'default')

migrate = Migrate(app, db)



@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@app.cli.command()
def deploy():
    upgrade()

