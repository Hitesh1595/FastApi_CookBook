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