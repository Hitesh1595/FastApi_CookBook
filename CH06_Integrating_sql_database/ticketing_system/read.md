In this chapter, we’re going to cover the following recipes:
• Setting up SQLAlchemy
• Implementing CRUD operations
• Working with migrations
• Handling relationships in SQL databases
• Optimizing SQL queries for performance
• Securing sensitive data in SQL databases
• Handling transactions and concurrency


$ pip install fastapi[all] "sqlalchemy>=2.0.0" aiosqlite

In this example, we have used an SQLite database by specifying the following:

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///.database.db"

However, you can use SQLAlchemy to interact with multiple SQL databases such as MySQL or
PostgreSQL by simply specifying the database driver, the asyncio-supported driver, and the
database address.
For example, for MySQL, the connection string would look like this:

mysql+aiomysql://user:password@host:port/dbname[?key=value&key=value...]

In this case, you need the aiomysql package installed in your environment.


You can check more on the official documentation pages:

• SQLAlchemy MySQL dialect: https://docs.sqlalchemy.org/en/20/dialects/mysql.html
• SQLAlchemy PostgreSQL dialect: https://docs.sqlalchemy.org/en/20/dialects/postgresql.html


pip install alembic

How to do it…
To configure Alembic and manage database migrations, go through the following steps.
1.The first step is to set up alembic. In the project root folder, run the following command in the command line:

$ alembic init alembic


folder before running the alembic init command.

2.Find the sqlalchemy.url variable and set the database URL to the following:
sqlalchemy.url = sqlite:///.database.db
This specifies that we are using an SQLite database If you use a different database, adjust it accordingly.

3.The alembic directory contains a folder version and an env.py file that has the variable for creating our database migrations.
Open the env.py file and find the target_metadata variable. Set its value to the metadata
of our application as follows:


from app.database import Base
target_metadata = Base.metadata


Execute the following command from the command line to create an initial migration:

$ alembic revision --autogenerate -m "Start database"

This will create a migration script automatically placed in the alembic/versions folder.

5.Make sure you removed the existing .database.db file, and let’s execute our first migration with the following command:

$ alembic upgrade head

This will automatically rebuild the .database.db file with the tickets table in it.


for history check
alembic history --verbose
