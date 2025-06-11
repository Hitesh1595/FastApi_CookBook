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



<!-- query------------------------------------------------------- -->

Improving SQL queries is a process that involves several steps. As with most optimization processes,
many steps are specific to the use case, but there are general rules that can help optimize SQL queries
overall, such as the following:
• Avoid N+1 queries
• Use the JOIN statement sparingly
• Minimize data to fetch
We will apply each with a significant example.


IMPORTANT

Different SQL databases may have different strengths and weaknesses in handling these factors,
depending on their architecture and features. For example, some SQL databases may support partitioning,
sharding, replication, or distributed processing, which can improve the scalability and availability of
data. Some SQL databases may offer more advanced query optimization techniques, such as cost-based
optimization, query rewriting, or query caching, which can reduce the execution time and resource
consumption of queries. Some SQL databases may implement different storage engines, transaction
models, or index types, which can affect the performance and consistency of data operations.
Therefore, when choosing an SQL database for a specific application, it is important to consider the
characteristics and requirements of the data and queries, and compare the capabilities and limitations of
the available SQL databases. A good way to do this is to benchmark the performance of SQL databases
using realistic datasets and queries and measure the relevant metrics, such as throughput, latency,
accuracy, and reliability. By doing so, one can find the optimal SQL database for the given scenario
and also identify potential areas for improvement in the database design and query formulation.




Securing sensitive data in SQL databases


Sensitive data, such as personal information, financial records, or confidential documents, is often stored in SQL databases for various applications and purposes.

$ pip install cryptography