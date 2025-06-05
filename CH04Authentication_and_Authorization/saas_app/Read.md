We will create the essential components of software as a service (SaaS) to help you learn practically
how to establish user registration systems, verify users, and handle sessions efficiently.

We’ll also
show you how to apply role-based access control (RBAC) to adjust user permissions and protect
API endpoints with API key authentication. The incorporation of third-party authentication using
external login services, such as GitHub, will demonstrate how to leverage existing platforms for user
authentication, simplifying the login process for your users.
Furthermore, you’ll add an extra layer of security by implementing "multi-factor authentication"
(MFA), ensuring that your application’s security is robust against various attack vectors.


In this chapter, we’re going to cover the following recipes:
• Setting up user registration
• Working with OAuth2 and JWT for authentication
• Setting up RBAC
• Using third-party authentication
• Implementing MFA
• Handling API key authentication
• Handling session cookies and logout functionality



$ pip install passlib[bcrypt]
$ pip install sqlalchemy>=2.0.0
$ pip install python-jose[cryptography]


for data migration in slq alchemy


pip install alembic
alembic init alembic

Open the alembic.ini file and find the line:

ini CopyEdit
sqlalchemy.url = sqlite:///./your.db


In alembic/env.py, find this block:

# from myapp import mymodel
# target_metadata = mymodel.Base.metadata


After adding or changing a field (like role in User), run:

alembic revision --autogenerate -m "Add role column to users"


Step 6: Apply the Migration to Update the DB

alembic upgrade head


example with default value

def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.Enum('basic', 'premium', name='role'),
            nullable=False,
            server_default='basic'  # <-- Add this ----------- this line
        )
    )



Bonus Tip: Clean Alembic Revisions (for dev only)

alembic downgrade base  # rollback all
rm alembic/versions/*.py  # delete old migration scripts
alembic revision --autogenerate -m "init roles"
alembic upgrade head

http://127.0.0.1:8000/github/auth/token
