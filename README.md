[![Coverage Status](https://coveralls.io/repos/andela-ijubril/bucketlist-api/badge.svg?branch=master&service=github)](https://coveralls.io/github/andela-ijubril/bucketlist-api?branch=master)
[![Build Status](https://travis-ci.org/andela-ijubril/bucketlist-api.svg?branch=master)](https://travis-ci.org/andela-ijubril/bucketlist-api)
Bucketlist Api
===============

This repository contains a working bucketlistApi written in Flask

Requirements
------------
To install and run this application, you need to have python installed on your machine.

Installation
------------

The commands below install the application and its dependencies:

    $ git clone https://github.com/andela-ijubril/bucketlist-api.git
    $ cd bucketlist-api    
    $ source venv/bin/activate
    (venv) pip install -r requirements.txt

Unit test
=========
-----------

To ensure that your installation was successful run python manage.py test:

(venv) $ python manage.py test

Running the app
---------------

    $python manage.py db init
    $python manage.py db migrate
    $python manage.py db upgrade
    $python manage.py runserver


Endpoints
------------

        
    -----------------------------------------------------------------------
    Endpoints                               Functionality
    ------------------------------------------------------------------------
    POST /auth/register                       Registers a user 
    POST /auth/login                          return a token to authenticated user 
    POST /bucketlists/                        create a new bucketlist 
    GET /bucketlists/                         List all the created bucket lists       
    GET /bucketlists/<id>                     Get single bucket list       
    PUT /bucketlists/<id>                     Update this bucket list   
    DELETE /bucketlists/<id>                  Delete this single bucket list   
    POST /bucketlists/<id>/items/             Create a new item in bucket list
    PUT /bucketlists/<id>/items/<item_id>     Update a bucket list item
    DELETE /bucketlists/<id>/items/<item_id>  Delete an item in a bucket list    
    ------------------------------------------------------------------------
   


###Request format
```

http://localhost:5000/api/v1/(Endpoints) e.g http://localhost:5000/api/v1/auth/register


```