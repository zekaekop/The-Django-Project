<h1>Running The Django Project</h1>

First of all if you are going to <a href = "https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project">Contribute</a>, you should create your own <a href="https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo">Fork</a> before starting to clone.
```git
git clone (Your Fork Url) # Ex: https://github.com/zekaekop/The-Django-Project.git
```

When you have cloned it in your working directory, you should create a <a href="https://docs.python.org/3/library/venv.html">Python Virtual Enviorment</a>
and install the requirements.txt located in the The-Django-Project folder.

```python
python -m venv C:\path\to\new\virtual\environment
```

And Activate the Virtual Enviorment by running <b>"venv\Scripts\activate"</b>.

```
pip install -r /path/to/requirements.txt
```

Apply database migrations.

```
python manage.py migrate
```

Create a superuser. (optional)

```
python manage.py createsuperuser
```

When your finished you can run.

```
python manage.py runserver
```

and it will be avaliable on your browser at "http://127.0.0.1:8000".

<hr>

<h1>WARNING: I will stop updating the fixtures, they wont work if its out of date. (You can still make your own fixtures.)</h1>

<h2>Using the sample database</h1>

By default you should get an emty database, but if you want to checkout the project without manually filling up all the data yourself.
You can use the sample db.

```
python manage.py loaddata db_sample.json 
```

And if you want to go back to the emty database you can do this.

```
python manage.py flush    
```

<hr>

<h2>Dumping a database</h1>

This is how i create the db_sample.json files, you can find more info about it <a href="https://docs.djangoproject.com/en/6.0/ref/django-admin/#django-admin-dumpdata">here</a>. <br>
But i advise using the manage.py file instead of django-admin.

```
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db_sample.json
```

This will dump your db data into a json file in your project directory.

<hr>

For more Information about the Contents you can find it <a href="/docs/Contents.md">here</a>.
<br>
Feel free to report any issues you have <a href="https://github.com/zekaekop/The-Django-Project/issues/new">here</a>.
