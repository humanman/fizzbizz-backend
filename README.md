# FizzBizz Booking App - Backend

This is the result of a solo sprint challenge:
 - Create single day booking app

## Usage

- Users can see meeting rooms availability

- Users can book meeting rooms by the hour (first come first served)

- Users can cancel their own reservations


- Check out the Front end over at [FizzBizz Front End](https://github.com/humanman/fizzbizz-frontend)

### Deployment

TODO:
 - Github Actions to implement CI/CD pattern via merges
 - Predeployment tests
 - write tests [Pytest](https://docs.pytest.org/en/stable/)

### Invocation

Endpoints:
- GET    - /{stage}/api/v1/user
- POST   - /{stage}/api/v1/user/new
- PUT    - /{stage}/api/v1/user/{username}
- DELETE - /{stage}/api/v1/user/{username}
- GET    - /{stage}/api/v1/booking
- POST   - /{stage}/api/v1/booking/new
- PUT    - /{stage}/api/v1/booking/{booking_id}
- DELETE - /{stage}/api/v1/booking/{booking_id}

functions:
- users: fizzbizz-backend-dev-users
- bookings: fizzbizz-backend-dev-bookings

### Local development

 - to test functionality on AWS:
  ``` serverless invoke --function {function name} -s {stage} --path {test.json}```

  - to test functionality locally:
  ``` serverless invoke local --function {function name} -s {stage} --path {test.json}```
      - This may require spinning up a local instance of dynamoDB or similar. See instructions [here](https://medium.com/better-programming/how-to-set-up-a-local-dynamodb-in-a-docker-container-and-perform-the-basic-putitem-getitem-38958237b968)

  - 'test.json' is a file containg the uri, http method, and relevent data:
  ```
  {
    "path": "api/v1/user/yoshi",
    "httpMethod": "DELETE",
    "body": {
      "username" : "yoshi",
      "email"    : "mario@nintendo.com"
    }
  }
  ```
  - If aws credentials are not set up, then uncomment/update `profile: {aws profile name}` in _serverlesss.yml_



Python Virtual Environment (venv)
  ```
  $python3 -m venv vent
  $source venv/bin/activate
  ```
Containerizes application dependencies 

You can invoke your function locally by using the following command:

### Bundling dependencies

In case you would like to include 3rd party dependencies, you will need to use a plugin called `serverless-python-requirements`. You can set it up by running the following command:

```bash
serverless plugin install -n serverless-python-requirements
```

Running the above will automatically add `serverless-python-requirements` to `plugins` section in your `serverless.yml` file and add it as a `devDependency` to `package.json` file. The `package.json` file will be automatically created if it doesn't exist beforehand. Now you will be able to add your dependencies to `requirements.txt` file (`Pipfile` and `pyproject.toml` is also supported but requires additional configuration) and they will be automatically injected to Lambda package during build process. For more details about the plugin's configuration, please refer to [official documentation](https://github.com/UnitedIncome/serverless-python-requirements).
