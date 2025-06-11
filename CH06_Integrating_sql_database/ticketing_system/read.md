# FastAPI SQLAlchemy Integration Guide

This chapter covers the following recipes:

* Setting up SQLAlchemy
* Implementing CRUD operations
* Working with migrations
* Handling relationships in SQL databases
* Optimizing SQL queries for performance
* Securing sensitive data in SQL databases
* Handling transactions and concurrency

---

## Installation

```bash
pip install fastapi[all] "sqlalchemy>=2.0.0" aiosqlite
pip install alembic
pip install cryptography
```

---

## Database Setup

### SQLite Configuration

```python
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///.database.db"
```

### MySQL Configuration

```python
SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://user:password@host:port/dbname[?key=value&key=value...]"
```

**Note:** For MySQL, you need to install the `aiomysql` package.

### Supported Databases

SQLAlchemy supports multiple SQL databases:
* SQLite
* MySQL
* PostgreSQL

---

## Migration Management with Alembic

### Initial Setup

1. **Initialize Alembic** in your project root:
   ```bash
   alembic init alembic
   ```

2. **Configure database URL** in `alembic.ini`:
   ```ini
   sqlalchemy.url = sqlite:///.database.db
   ```

3. **Set target metadata** in `env.py`:
   ```python
   from app.database import Base
   target_metadata = Base.metadata
   ```

### Creating and Running Migrations

**Generate migration:**
```bash
alembic revision --autogenerate -m "Start database"
```

**Apply migration:**
```bash
alembic upgrade head
```

**Check migration history:**
```bash
alembic history --verbose
```

**Important:** Remove existing database files before running your first migration.

---

## Query Optimization

### Key Optimization Principles

* **Avoid N+1 queries** - Use eager loading with `joinedload()` or `selectinload()`
* **Use JOIN statements sparingly** - Only join when necessary
* **Minimize data to fetch** - Select only required columns and use pagination

### Database-Specific Considerations

Different SQL databases have varying strengths:

* **Partitioning & Sharding** - Some databases support horizontal scaling
* **Query Optimization** - Advanced techniques like cost-based optimization
* **Storage Engines** - Different engines offer various performance characteristics
* **Indexing** - Various index types for different use cases

### Performance Testing

When choosing a database:
* Benchmark with realistic datasets
* Measure throughput, latency, accuracy, and reliability
* Compare capabilities and limitations
* Test under expected load conditions

---

## Security Best Practices

### Protecting Sensitive Data

Sensitive data types requiring protection:
* Personal information
* Financial records
* Confidential documents
* Authentication credentials

### Security Measures

* Encrypt sensitive data before storing
* Use proper authentication and authorization
* Implement input validation and sanitization
* Follow principle of least privilege

---

## Transaction Management

### Concurrency Control

#### Lock Levels
* **Database-level** - SQLite only supports this level
* **Table-level** - Supported by most databases
* **Row-level** - Available in PostgreSQL and others

#### Isolation Levels

The SQL standard defines four isolation levels:

**1. READ UNCOMMITTED**
* Allows dirty reads
* Highest concurrency, lowest consistency
* Non-repeatable and phantom reads possible

**2. READ COMMITTED**
* Only sees committed changes
* Prevents dirty reads
* Balanced concurrency and consistency

**3. REPEATABLE READ**
* Consistent snapshot throughout transaction
* Prevents non-repeatable reads
* Phantom reads still possible

**4. SERIALIZABLE**
* Highest consistency level
* Transactions appear to execute serially
* May reduce concurrency due to locking

### Setting Isolation Levels

Example for PostgreSQL:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "postgresql+psycopg2://scott:tiger@localhost/test",
    isolation_level="REPEATABLE READ",
)
Session = sessionmaker(engine)
```

### Database Support Matrix

| Database   | Isolation Levels Supported |
|------------|----------------------------|
| SQLite     | Limited isolation support  |
| MySQL      | All four levels           |
| PostgreSQL | All four levels           |

---

## Additional Resources

### Official Documentation

* [SQLAlchemy MySQL Dialect](https://docs.sqlalchemy.org/en/20/dialects/mysql.html)
* [SQLAlchemy PostgreSQL Dialect](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)

### Best Practices

* Understand your database's locking mechanisms
* Choose appropriate isolation levels for your use case
* Consider business logic requirements when designing transactions
* Test concurrency scenarios thoroughly
* Monitor performance in production environments