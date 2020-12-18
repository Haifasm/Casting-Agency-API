# Casting Agency
This is a simple application API for managing movie and actor records in a PostgreSQL database.

##requirments

##db Setup
createdb agency

##Auth0 Setup
1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:actor`
    - `get:movie`
    - `post:actor`
    - `post:movie`
    - `patch:actor`
    - `patch:movie`
    - `delete:actor`
    - `delete:movie`
6. Create new roles and add the required permissions according to the table below:
    
    | Permission/Role  | Casting Assistant | Casting Director | Executive Producer |
    | ------------- | ------------- | ------------- | ------------- |
    | get:actor | ✔️ | ✔️ | ✔️ |
    | get:movie | ✔️ | ✔️ | ✔️ |
    | post:actor | | ✔️ | ✔️ |
    | post:movie | | | ✔️ |
    | patch:actor | | ✔️ | ✔️ |
    | patch:movie | | ✔️ | ✔️ |
    | delete:actor | | ✔️ | ✔️ |
    | delete:movie | | | ✔️ |

7. Get JWT tokens: 
    ⋅⋅1. Enter the correct AUTH0 URI as follows:
    ```
     https://{YOUR_DOMAIN}/authorize?audience={API_AUDIENCE}&response_type=token&client_id={AUTHO_CLIENT_ID}&redirect_uri={CALLBACK_URL}
    ```
    ⋅⋅⋅* {YOUR_DOMAIN} = 
    ⋅⋅⋅* {API_AUDIENCE} = 
    ⋅⋅⋅* {AUTHO_CLIENT_ID} = 
    ⋅⋅⋅* {CALLBACK_URL} = 

    ⋅⋅2.
    ⋅⋅2.
    ⋅⋅2.
    ⋅⋅2.