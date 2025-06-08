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