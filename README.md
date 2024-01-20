# Fyle Backend Challenge

## About me
Hello I am Arman from india. This is the solution of Fyle Backend Challenge for internship.


#
## Step 1 : Building the image
This will build the docker image from the Dockerfile
```
docker build -t fyle-interview-intern-backend .
```

#
## Step 2 : Running the image
This will start the container
```
docker run -d -p 7755:7755 fyle-interview-intern-backend
```

#
## Step 3 : Past container id in the following command
This will start a terminal from whitch application can be controlled.
```
docker exec -it $id /bin/sh
```

#
### Run Tests
You can run tests in the terminal which you start in step 3
```
pytest -vvv -s tests/

# for test coverage report
# pytest --cov
# open htmlcov/index.html
```

#
### Remember that
first time all test will be passed. 
Next time because previousally database modified and in tests values are hardcoded so all tests will not passed