<!DOCTYPE html>
<html lang="text/html">
  <link rel="stylesheet" type="text/css" href="drf_spectacular_stylesheet.css">
  <head>
    <title>LifeLogger API</title>
    <meta charset="utf-8">
  </head>
  <body>
    <p>
      This Swagger API describes a website called LifeLogger. With LifeLogger, you can create an account, use JWT authentication, describe habits, and track vitals like weight and other bodily stats. Users can subscribe to habits to monitor personal achievements.
    </p>
    <details>
      <summary>Authentication</summary>
      <p>
        This section describes how to authenticate with the LifeLogger API using JSON Web Tokens (JWT).
      </p>
      <p>
        To authenticate with the LifeLogger API, you'll need to obtain a JWT from the server by sending a POST request to the <code>/auth/token/</code> endpoint with your username and password in the request body. The server will respond with a JWT, which you can use to make authenticated requests to the API.
      </p>
      <p>
        To make an authenticated request to the API, include the JWT in the <code>Authorization</code> header of your HTTP request using the following format:
      </p>
      <pre><code>Authorization: Bearer &lt;JWT&gt;</code></pre>
      <p>
        Replace &lt;JWT&gt; with the JWT obtained from the server. Note that the JWT should be prefixed with the word "Bearer" and a space.
      </p>
    </details>
    <details>
      <summary>Habits</summary>
      <p>
        This section describes how to create and manage habits in LifeLogger.
      </p>
      <!-- Markdown content for the Habits section -->
    </details>
    <details>
      <summary>Subscriptions</summary>
      <p>
        This section describes how to subscribe to habits in LifeLogger.
      </p>
      <!-- Markdown content for the Subscriptions section -->
    </details>
  </body>
</html>