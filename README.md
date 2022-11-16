# COMP3278 Database Project

HKU ICMS Intelligent Course Management System

## Setting up
### Install dependencies
1. Install `pipenv` using `pip`: `pip install pipenv`
2. Activate the virtual environment: `pipenv shell`
3. Install the packages needed: `pipenv install`

### Configure MySQL database

1. Install MySQL with username `root` and password `comp3278` (can be modified in `settings.py`)
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

If the project failed to run due to missing `/usr/local/lib/libmysqlclient.21.dylib`,

1. Make sure you have MySQL installed at `/usr/local/mysql/`
2. Make a symbolic link for that missing file to the one in the MySQL folder by
   
   `ln -s /usr/local/mysql/lib/libmysqlclient.21.dylib /usr/local/lib/libmysqlclient.21.dylib`

### Default admin account
Username: `admin@cs.hku.hk`

Password: `comp3278`

Change the password right after the first login

### Configure an email address to send emails
1. Open `icms/settings.py`
2. Edit `EMAIL_HOST`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD`

### Add a new user
1. Go to the admin page `[hostname]/admin`
2. Go to Users and add a new user (email address)

### Add a new face for face recognition login
1. Go to `face_recognition/` and run
   
   `python face_capture.py -u [EMAIL_ADDRESS] -n [NUMBER_OF_IMAGES]`

2. Train the model: `python train.py`

## Run the server
1. Make migrations (if there are any changes to the database schemas): `python manage.py makemigrations`
2. Apply migrations (if there are any): `python manage.py migrate`
3. Run the server: `python manage.py runserver`
