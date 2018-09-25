Testing a web app and rest services apis
########################################
This project contains:

1- A web app that allows to add users and show them in a list, to achieve that,
it uses rest services calls developed using flask. The data is persisted in a mongodb.

2- The corresponding ui tests using selenium and behave.

3- The corresponding rest service api tests using pytest.

All these project components can be deployed as docker containers and the relationship between them can be seen
in docker-compose.yaml file

Running tests using docker-compose
==================================
1- Install docker-compose in your system, then:

::

  $ git clone https://github.com/heber013/userapp-testing
  $ cd userapp-testing
  $ sudo docker-compose up --build

By default it will run all tests: the UI and rest service ones.
To check UI tests results: tests/ui/docker_outputs
To check rest service tests results: tests/api/docker_outputs
First execution is slow since docker-compose has to download all the images.

|

It is possible to run only UI tests:

::

    $ docker-compose up --build apptests

The same for running only rest service api test:

::

    $ docker-compose up --build apitests


After any execution, it’s possible to stop the running containers and delete them with a command:

::

    $ docker-compose down
