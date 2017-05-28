# Catalog

An application that provides a list of items within a variety of categories as well as provides a third-party user authentication and authorization system (Google+ and Facebook) using OAuth2 framework. Registered users have the ability to post, edit and delete their own items. 
The project also implements JSON endpoints that serve the same information as displayed in the HTML endpoints, has CRUD functionality for image handling and CSRF protection on the CRUD operations. The web application was successfully deployed to Amazon Web Services.

## Complete URL

http://ec2-54-197-202-119.compute-1.amazonaws.com

## Getting Started

### Prerequisites

The software you need to install:

[Vagrant](https://www.vagrantup.com/)

[VirtualBox](https://www.virtualbox.org/)

Also in order for the OAuth system to work follow the links below for Google+ and Facebook login to get and replace:

Inside `fb_client_secrets.json`(line 3,4) and `login.html`(line 81):

`FB_APP_ID_GOES_HERE `- with your Facebook app id

`FB_APP_SECRET_GOES_HERE`- with your Facebook app secret

Inside `client_secrets.json`(line 1) and `login.html`(line 29):

`GOOGLE_CLIENT_ID_GOES_HERE`- with your Google client id

`GOOGLE_CLIENT_SECRET_GOES_HERE`- with your Google client secret

### Steps you need to take:

1. Install Vagrant and VirtualBox on your machine
2. Clone the project
3. Launch the Vagrant VM

`vagrant up`

4. SSH into the VM

`vagrant ssh`

5. Navigate to `catalog` project using CLI

6. Create the database

`python database_setup.py`

7. Populate the database(optional)

`python lotsofitems.py`

8. Run your application within the VM

`python project.py`

9. Access and test your application by visiting `http://localhost:5001` locally
10. JSON Endpoins at (replace [CATEGORY_ID] and [ITEM_ID] with integers):

 `* http://localhost:5001/catalog.JSON`  
 `* http://localhost:5001/catalog/category/[CATEGORY_ID].JSON`  
 `* http://localhost:5001/catalog/item/[ITEM_ID].JSON`

### Ports used:

```
guest: 8000, host: 8001
guest: 8080, host: 8081
guest: 5000, host: 5001
```

## Built With

* [Python](https://www.python.org/) - Programming language
* [SQLite](https://www.sqlite.org/) - SQL database engine
* [SQLAlchemy](https://www.sqlalchemy.org/) - Object Relational Mapper
* [Flask](http://flask.pocoo.org/) - Web Framework
* [Facebook login](https://developers.facebook.com/docs/facebook-login) - Third party authentication and authorization service
* [Google+ login](https://developers.google.com/+/web/api/rest/oauth) - Third party authentication and authorization service


## Authors

* **Iurie Popovici** - *Initial work*
