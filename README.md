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
   


##Endpoints description

###Authentication

**Register a user.** 

POST: api/v1/auth/register/


Request body
```
	{
	"username": "username",
	"email": "username@email.com",
	"password": "password"

	}
```
Response body
```
	{
      "status": "(Username) has successfully registered"
    }
```
    

**Returns a token for the authenticated user.**

POST: /api/v1/auth/login/

Request body
```
	{
	"username": "username",
	"password": "password"

	}
```
Response body
```
	{
      "status": "token generated successfully",
      "token": "(token returned)"
    }
```
    
###Bucketlist    

**Create a new bucketlist.**

POST: /api/v1/bucketlist/


You must pass a token for this request

Request body
```
	{
	"name": "first bucketlist"	
	}
```
Response body
```
	 {
      "message": "Your bucketlist was created successfully",
      "Bucketlist": {
        "name": "first bucketlist",
        "date_modified": "(date and time created in this case)",
        "created_by": {
          "username": "(bucket list creator id)"
        },
        "item_count": (current count of the items in the bucketlist),
        "date_created": "(date and time created)",
        "id": (the id of the bucketlist)
      }
    }
```
 
    
**Get the bucketlists of the current authenticated user.**

GET: api/v1/bucketlists/


You must pass a token for this request

Response body
```  
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
```      

   
You can also pass some arguments like page, limit and q in the request
```
    GET: /api/v1/bucketlists/?q=something (to search by name)
    GET: /api/v1/bucketlists/?page=2 (to move to the next page for the current bucketlist returned it is 1 by default)
    GET: /api/v1/bucketlists/?limit=10 (to limit the reponse to 10 bucketlist)
```

    
**Get a single bucketlist.**

GET: /api/v1/bucketlists/26/

You must pass a token for this request

Response body
``` 
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
```
    
**Update a single bucketlist.**

PUT: /api/v1/bucketlists/26/

You must pass a token for this request

Response body
```
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
```    
    
**Delete a single bucketlist.**

DELETE: /api/v1/bucketlists/26/

You must pass a token for this request

Response body
```    
    {
      "message": "Bucketlist successfully deleted"
    }
```    
    
**Create a new item.** 

POST: /api/v1/bucketlists/(id)/items/

You must pass a token for this request

Request body
```
	{
		"name": "first item"
	}
```
Response body    
    
``` 
    {
      "Item": {
        "url": "http://localhost:5000/api/v1/bucketlists/(id)/",
        "date_created": "(date it was created )",
        "date_modified": "(date it was modified)",
        "id": (the id of the item),
        "name": "first awesome item to put in the list"
      },
      "message": "Your bucketlist Items was created successfully"
    }
```    

**Update a single item.**

PUT: /api/v1/bucketlists/(id)/items/(item_id)/

You must pass a token for this request

Request body
```
	{
		"name": "first item updated"
	}
```
Response body
```
	{
      "Item": {
        "url": "http://localhost:5000/api/v1/bucketlists/26/",
        "date_created": "(date it was created )",
        "date_modified": "(date it was modified)",
        "id": (the id of the item),
        "name": "first awesome item to be edited in the list"
      }
    }
```	

   
**Delete a single item.**

DELETE: /api/v1/bucketlists/(id)/items/(item_id)/

You must pass a token for this request

Response body
```        
    {
      "message": "Item successfully deleted"
    }
```

