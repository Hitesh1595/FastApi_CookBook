# FastAPI NoSQL Database Integration Guide

This chapter covers how to perform create, read, update and delete (CRUD) operations, work with indexes for performance optimization, and handle relationships in NoSQL databases. Additionally, you will learn how to integrate FastAPI with Elasticsearch for powerful search capabilities, secure sensitive data, and implement caching using Redis.

By the end of this chapter, you will have a solid understanding of how to effectively use NoSQL databases with FastAPI to improve the performance and functionality of your applications.

In this chapter, we're going to cover the following recipes:

* Setting up MongoDB with FastAPI
* CRUD operations in MongoDB
* Handling relationships in NoSQL databases
* Working with indexes in MongoDB
* Exposing sensitive data from NoSQL databases
* Integrating FastAPI with Elasticsearch
* Using Redis for caching in FastAPI

---

## Installation

```bash
pip install "elasticsearch>=8,<9"
pip install redis
```

---

## Working with MongoDB Indexes

### Performance Optimization

**Important Note:** By using the `explanation_query` variable, you can check the difference in execution time. However, you need a huge number of documents in your collection to appreciate the improvement.

### Index Types

MongoDB allows you to create various types of indexes:

* **Text indexes** - For search over text fields like artist names
* **Numbered indexes** - For numeric fields like year of release
* **2D sphere indexes** - For geospatial data
* **Compound indexes** - For multiple fields

---

## Securing Sensitive Data in NoSQL Databases

### Data Masking

Data masking is a crucial security technique that helps protect sensitive information by replacing real data with fictitious but realistic data.

### Additional Security Layers

Beyond data masking, additional security layers include:

* **Encryption at rest** - Encrypts data stored in your MongoDB database
* **Encryption in transit** - Encrypts data transmitted between application and server
* **Role-Based Access Control (RBAC)** - Restricts access based on user roles

### Enterprise MongoDB Security Features

**Encryption at Rest:**
* Built-in encryption capabilities through dedicated storage engine
* Data encrypted on disk, unreadable without proper encryption keys
* Prevents unauthorized access to sensitive information

**Encryption in Transit:**
* Uses Transport Layer Security (TLS)
* Encrypts data sent over network between application and MongoDB server
* Prevents eavesdropping and tampering

**Role-Based Access Control:**
* Robust authentication and authorization mechanisms
* Control access to databases, collections, and documents
* Create user accounts with different roles and privileges
* Ensure only authorized users can access sensitive data

---

## Elasticsearch Integration

### System Installation

For Ubuntu/Debian systems, follow the installation guide:
* [Install Elasticsearch on Ubuntu](https://phoenixnap.com/kb/install-elasticsearch-ubuntu)

### Docker Installation (Alternative)

```bash
docker run -d --name elasticsearch \
  -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  elasticsearch:8.11.0
```

### Verify Installation

```bash
curl http://localhost:9200
```

---

## Redis for Caching

### Installation Requirements

To follow along with Redis caching, you need a running Redis instance reachable at `http://localhost:6379`.

### FastAPI Cache Library

There is a promising library `fastapi-cache` which makes caching in FastAPI very easy:
* [FastAPI Cache GitHub Repository](https://github.com/long2ice/fastapi-cache)

**Features:**
* Supports several caching databases including Redis and in-memory caching
* Simple endpoint decorators for caching parameters
* Configurable time to live, encoder, and cache response headers

---

## Additional Resources

### MongoDB Documentation

* [MongoDB Indexes](https://www.mongodb.com/docs/v5.3/indexes/)
* [MongoDB Text Search](https://www.mongodb.com/docs/manual/core/link-text-indexes/)
* [MongoDB Aggregations Quickstart](https://www.mongodb.com/developer/languages/python/python-quickstart-aggregation/)
* [MongoDB Views Documentation](https://www.mongodb.com/docs/manual/core/views/)
* [Aggregation Stage Reference](https://www.mongodb.com/docs/manual/reference/operator/aggregation-pipeline/)

### Elasticsearch Documentation

* [Elasticsearch Python Client](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html)
* [Using Asyncio with Elasticsearch](https://elasticsearch-py.readthedocs.io/en/7.x/async.html)
* [Index API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html)
* [Mapping Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html)
* [Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)

### Redis Documentation

* [Redis Python Client](https://redis.io/docs/connect/clients/python/)
* [Redis Python Asynchronous Client](https://redis-py.readthedocs.io/en/stable/examples/asyncio_examples.html)

### Examples and Advanced Resources

* [MongoDB Data Masking Example](https://github.com/pkdone/mongo-data-masking?tab=readme-ov-file)
* [Practical MongoDB Aggregation Book](https://www.practical-mongodb-aggregations.com) - Free comprehensive guide

### MongoDB Aggregations and Views

MongoDB provides powerful aggregation and view capabilities for:
* Complex data processing
* Data transformation
* Advanced data masking through database aggregations
* Creating reusable data views

**Note:** The choice of using enterprise security features is at the discretion of software architects based on specific application requirements and security needs.