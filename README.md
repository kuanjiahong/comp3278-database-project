# comp3278-database-project

comp3278-database-project

**Setting up**

1. Install `pipenv` using `pip`: `pip install pipenv`
2. Activate the virtual environment: `pipenv shell`
3. Install the packages needed: `pipenv install`

**Run the program**
1. Apply migration (if there is any): `python manage.py migrate`
2. Run the server: `python manage.py runserver`

**Configure MySQL database**

1. Install MySQL with username `root` and password `comp3278` (can be modified in `settings.py` --> see NOTES below)
2. Create a database named `comp3278`

   `mysql -u root -p`

   `create database comp3278;`

   `exit;`

3. Load db.sql to database `comp3278`

   `mysql -u root -p comp3278 < db.sql`

If you wish to use your existing MySQL database,
1. Go to `settings.py` under `icms` directory
2. Ctrl-F search `DATABASES`
3. Modify `NAME` (i.e. your database name), `USER`, `PASSWORD` to your own settings

**NOTES:**

If the project failed to run due to missing `/usr/local/lib/libmysqlclient.21.dylib`,

1. Make sure you have MySQL installed at `/usr/local/mysql/`
2. Make a symbolic link for that missing file to the one in the MySQL folder by
   
   `ln -s /usr/local/mysql/lib/libmysqlclient.21.dylib /usr/local/lib/libmysqlclient.21.dylib`


