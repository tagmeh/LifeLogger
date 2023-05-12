<link rel="stylesheet" type="text/css" href="drf_spectacular_stylesheet.css">

## Welcome to the LifeLogger API Swagger page.  

## Getting Started
All links open in a new tab, this is a known issue. [Issue #3473](https://github.com/swagger-api/swagger-ui/issues/3473) 

### Creating a new account
<details>
    <summary>Click to expand</summary>  
    To get started, [create an account](#/Users/create-users) (Users > Create)  
</details>

### Authentication
<details>
    <summary>Click to expand</summary>  

Authentication is done using [JSON Web Token](https://jwt.io/introduction/).  
This project uses [<b>Simple JWT</b>](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)  
The endpoints are found under the <b>"api"</b> section.


#### /token/

Authenticate with this endpoint using your login credentials.  
The response will contain <b>access</b> and <b>refresh</b> keys.  
You'll use the <b>access</b> value in the header to authenticate future calls.  

Header: `Authorization: Bearer eyJhbGciOiJIUI1NiIsInR5cC6IkpXVCJ9.ey0b2tlbl90eXBljoiYWNjZXNzIiwiZXhwIjoxNjgzODU5NzM3LCJpYXQiOjE2ODM4NTk0MzcsImpaSI6ImU1jFkZDU2NYwZjQxYmFiNjyNzM2NGYyZDhlMjI2IiwidXNlcl9pZCI6MX0.s0MEQKgYqWAiwgtw2bYQa0Ou5rWfD20wz4PWGn3eU`

#### /token/refresh 

Use your <b>refresh</b> value to "refresh" your <b>access</b> token, and revalidate it for a few more minutes.  
The <b>refresh</b> token will be valid for a few days, whereas the <b>access</b> token will only be valid for 
a few minutes, at which point, you'll need to reauthenticate with the <b>/token/</b> endpoint.

</details>

### Habits
This section is about tracking habits. A user can "subscribe" or create a habit that they want to work on. Habits 
can be good or bad, with the assumption that users want to work towards good habits, and work on stopping bad habits.  

Permissions have yet to be ironed out (2023-05-11) for exactly what a user can do.  

However, the idea is that a user subscribes to an existing or new habit using the 

### Vitals