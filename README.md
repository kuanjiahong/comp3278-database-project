# comp3278-database-project
comp3278-database-project


Setting up

1. Install `pipenv` using `pip`: `pip install pipenv`
2. Activate the virtual environment: `pipenv shell`
3. Install the packages needed: `pipenv install`
4. Run the server: `python manage.py runserver`

Configure MySQL database
1. Install MySQL with username `root` and password `comp3278`
2. Create a database named `comp3278`

    `mysql -u root -p`
    
    `create database comp3278;`
    
    `exit;`
3. Load db.sql to database `comp3278`

    `mysql -u root -p comp3278 < db.sql`

NOTES: If the project failed to run due to missing `/usr/local/lib/libmysqlclient.21.dylib`, make sure you have MySQL installed at `/usr/local/mysql/`, then make a symbolic link for that missing file to the one in the MySQL folder by

    `ln -s /usr/local/mysql/lib/libmysqlclient.21.dylib /usr/local/lib/libmysqlclient.21.dylib`