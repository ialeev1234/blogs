# installing 

pip install -r requirements.txt

# running

./manage.py runserver 0.0.0.0:5000

# testing 

./manage.py test

In every application placed 'tests' folder with unittests.  
Every test named by method which it is testing.
These unittests shows how correctly works our RestAPI methods.
We send some data to endpoints and check equality of results and expectations.

Last unittest in the Blogs application for task 5 (retrieving all articles of a Blog). 