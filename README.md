# Pitchme_QA_test

## Cover API with pytest Test Cases
You are provided with Pydantic schemas for User and Post entities, as well as Pydantic some schemas for request and response bodies.

The task is to come up with test cases and cover the following endpoints with tests:

**User Endpoints:**
- **GET /users:** Returns a list of all users.
- **GET /users/{id}:** Returns information about the user with the specified identifier.
- **POST /users:** Creates a new user. User data (name, surname, email, etc.) is passed in the request body.
- **PUT /users/{id}:** Updates user information based on the specified identifier. Data for updating is passed in the request body.
- **DELETE /users/{id}:** Deletes a user based on the specified identifier.

**Post Endpoints:**
- **GET /posts:** Returns a list of all posts.
- **GET /posts/{id}:** Returns information about the post with the specified identifier.
- **POST /posts:** Creates a new post. Post data (title, text, etc.) is passed in the request body.
- **PUT /posts/{id}:** Updates post information based on the specified identifier. Data for updating is passed in the request body. The author of the post cannot be changed.
- **DELETE /posts/{id}:** Deletes a post based on the specified identifier.

### Bonus Task
* Mock API responses. For example, using the `monkeypatch` library.

## Submission Process
* Fork this repository and create a pull request upon completion.
* If the fork is private, invite arexp19@gmail.com to access it.

## Technical Restrictions
* Python 3.9
* Built-in libraries + requirements.txt
