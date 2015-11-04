[![Coverage Status](https://coveralls.io/repos/andela-ijubril/bucketlist-api/badge.svg?branch=master&service=github)](https://coveralls.io/github/andela-ijubril/bucketlist-api?branch=master)
[![Build Status](https://travis-ci.org/andela-ijubril/bucketlist-api.svg?branch=master)](https://travis-ci.org/andela-ijubril/bucketlist-api)
[![Requirements Status](https://requires.io/github/andela-ijubril/bucketlist-api/requirements.svg?branch=master)](https://requires.io/github/andela-ijubril/bucketlist-api/requirements/?branch=master)
Bucketlist Api
===============

This repository contains a working bucketlistApi written in Flask

Requirements
------------
To install and run this application, you need to have python installed on your machine.

Installation
------------

To install run virtualenv (name_of_your_virtual_environment)
Activate the virtual environment
clone the repo
cd bucketlist-api
pip install -r requirements.txt

Unit test
---------
To ensure that your installation was successful run python manage.py test

Running the app
---------------

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

