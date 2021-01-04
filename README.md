# Users Service

This service is responsible for storing and processing information about users of the system, it also provides methods to authorize existing users and register new ones.

The service consists of 2 components:

1. **UsersService** – Python script
2. **MongoDB** – Database



The service provides only gRPC API.

**All API methods can return:**

1. **code**=500, **message**="An internal server error has occurred."



## IsExist

Checks the existence of a user with the specified username.

#### Parameters:

Receives a message of User type.

1. **username**. Unique user login in the system.

#### Result:

Returns a message of Response type.

1. **code**=200, **message**="An account with this username already exists."
2. **code**=404, **message**="An account with this username not found."
3. **code**=422, **message**="Username parameter is missing."



## Create

Creates a new user.

#### Parameters:

Receives a message of User type.

1. **username**. Unique user login in the system.
2. **first_name**.
3. **last_name**.
4. **password**.

#### Result:

Returns a message of ResponseWithUser type.

1. **status**=(**code**=201, **message**="User account has been created successfully."), **user**=(username, first_name, last_name, admin)
2. **status**=(**code**=409, **message**="That username is taken. Please choose a different one.")
3. **status**=(**code**=422, **message**="First name, last name, username and password parameters are required.")



## Verify

Verifies username and password.

#### Parameters:

Receives a message of User type.

1. **username**. Unique user login in the system.
2. **password**.

#### Result:

Returns a message of ResponseWithUser type.

1. **status**=(**code**=200, **message**="Username and password are correct."), **user**=(username, first_name, last_name, admin)
2. **status**=(**code**=401, **message**="Incorrect username or password.")
3. **status**=(**code**=422, **message**="Username and password parameters are required.")



## Info

Returns information about the user.

#### Parameters:

Receives a message of User type.

1. **username**. Unique user login in the system.

#### Result:

Returns a message of ResponseWithUser type.

1. **status**=(**code**=200, **message**="User with this username exists."), **user**=(username, first_name, last_name, admin)
2. **status**=(**code**=404, **message**="User with this username not found.")
3. **status**=(**code**=422, **message**="Username parameter is required.")


**The reported project was supported by RFBR, research project No. 18-07-01224**
