#!/usr/bin/env python
from flask import Flask, g, jsonify
from flask.ext.script import Manager
from api import create_app
from api.models import db, User, Bucketlist, Item
from flask.ext.migrate import Migrate, MigrateCommand
from flask import url_for

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()

