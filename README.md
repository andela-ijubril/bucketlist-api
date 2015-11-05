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

        
    ------------------------------------------------------------------------------------------------------
    Endpoints                               Functionality                               Public Access
    ------------------------------------------------------------------------------------------------------
    POST /auth/register                       Registers a user                           TRUE   
    POST /auth/login                          return a token to authenticated user       TRUE   
    POST /bucketlist/                        create a new bucketlist                     FALSE   
    GET /bucketlists/                         List all the created bucket lists          FALSE   
    GET /bucketlists/<id>                     Get single bucket list                     FALSE   
    PUT /bucketlists/<id>                     Update this bucket list                    FALSE   
    DELETE /bucketlists/<id>                  Delete this single bucket list             FALSE   
    POST /bucketlists/<id>/items/             Create a new item in bucket list           FALSE   
    PUT /bucketlists/<id>/items/<item_id>     Update a bucket list item                  FALSE   
    DELETE /bucketlists/<id>/items/<item_id>  Delete an item in a bucket list            FALSE   
    -------------------------------------------------------------------------------------------------------
   


###Endpoints description

    
POST http://localhost:5000/api/v1/auth/register/

Registers a user 
```    
    
    PARAMETERS
    
    username (compulsory)
    email (compulsory)
    password (compulsory)
    
    RESPONSE
    {
      "status": "(Username) has successfully registered"
    }
    
    
POST http://localhost:5000/api/v1/auth/login/

Returns a token for the authenticated user
    
    PARAMETERS
    
    username (compulsory)
    password (compulsory)
    
    RESPONSE
    
    {
      "status": "token generated successfully",
      "token": "(token returned)"
    }
    
POST http://localhost:5000/api/v1/bucketlist/

create a new bucketlist for the current authenticated user

you must pass a token for this request
    
    PARAMETERS
    name    (compulsory)
    
    RESPONSE
    {
      "message": "Your bucketlist was created successfully",
      "Bucketlist": {
        "name": "(whatever name you gave to your bucketlist)",
        "date_modified": "(date and time created in this case)",
        "created_by": {
          "username": "(bucket list creator id)"
        },
        "item_count": (current count of the items in the bucketlist),
        "date_created": "(date and time created)",
        "id": (the id of the bucketlist)
      }
    }
    
    
GET http://localhost:5000/api/v1/bucketlists/

get the bucketlists of the current authenticated user

you must pass a token for this request
    
    
    RESPONSE
    {
      "total": 1,
      "next_url": null,
      "bucketlists": [
        {
          "name": "awesome bucketlist that i want to create for the documentation",
          "date_modified": "(date it was modified or created as the case may be)",
          "created_by": {
            "username": "(user id)"
          },
          "item_count": 0,
          "date_created": "(date created )",
          "id": 26
        }
      ],
      "current_page": 1,
      "prev_url": null
    }
    
    you can also pass some arguments like page, limit and q in the request
    http://127.0.0.1:5000/api/v1/bucketlists/?q=something (to search by name)
    http://127.0.0.1:5000/api/v1/bucketlists/?page=2 (to move to the next page for the current bucketlist returned it is 1 by default)
    http://127.0.0.1:5000/api/v1/bucketlists/?limit=10 (to limit the reponse to 10 bucketlist)
    
    
GET http://localhost:5000/api/v1/bucketlists/26/

get a single bucketlist that correspond to the id passed for the authenticated user

you must pass a token for this request
    
    RESPONSE
    {
      "Bucketlist": {
        "name": "awesome bucketlist that i want to create for the documentation",
        "date_modified": "(date it was modified or created as the case may be)",
        "created_by": {
          "username": "(user id)"
        },
        "item_count": 0,
        "date_created": "(date created )",
        "id": 26
      }
    }
    
PUT http://localhost:5000/api/v1/bucketlists/26/

Update a single bucketlist that correspond to the id passed for the authenticated user

you must pass a token for this request
    
    PARAMETERS
    name    (compulsory)
    
    RESPONSE
    {
      "Bucketlist": {
        "name": "The edited name",
        "date_modified": "(date it was modified)",
        "created_by": {
          "username": "(user id)"
        },
        "item_count": 0,
        "date_created": "(date created )",
        "id": 26
      }
    }
    
    
DELETE http://localhost:5000/api/v1/bucketlists/26/

Deletes a single bucketlist that correspond to the id passed for the authenticated user

you must pass a token for this request
    
    RESPONSE
    {
      "message": "Bucketlist successfully deleted"
    }
    
    
POST http://localhost:5000/api/v1/bucketlists/(id)/items/

create a new item for a particular bucketlist if the user is the owner of the bucketlist for the current authenticated user

you must pass a token for this request
    
    PARAMETERS
    name    (compulsory)
    
    RESPONSE
    {
      "Item": {
        "url": "http://localhost:5000/api/v1/bucketlists/<id>/",
        "date_created": "(date it was created )",
        "date_modified": "(date it was modified)",
        "id": (the id of the item),
        "name": "first awesome item to put in the list"
      },
      "message": "Your bucketlist Items was created successfully"
    }
    
    
PUT http://localhost:5000/api/v1/bucketlists/(id)/items/(item_id)/

Update a single item in a bucketlist for the authenticated user

you must pass a token for this request
    
    PARAMETERS
    name    (compulsory)
    
    RESPONSE
    
    {
      "Item": {
        "url": "http://localhost:5000/api/v1/bucketlists/26/",
        "date_created": "(date it was created )",
        "date_modified": "(date it was modified)",
        "id": (the id of the item),
        "name": "first awesome item to be edited in the list"
      }
    }
    
    
DELETE http://localhost:5000/api/v1/bucketlists/(id)/items/(item_id)/

Delete a single item in a bucketlist for the authenticated user

you must pass a token for this request
    
    RESPONSE
    {
      "message": "Item successfully deleted"
    }


```