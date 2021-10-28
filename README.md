In the exercise it mentions nothing is installed, but I hope it is ok if I take for granted 
tools like docker and python3 as being installed. If not: 
    docker: https://docs.docker.com/desktop/mac/install/
    python3: https://www.python.org/downloads/macos/ (or use brew and type: brew install python)
    pip comes with python
    libraries will be installed via requirements.txt by docker
    CMake: https://cmake.org/install/ (or use brew and type: brew install cmake)

I use CMake to make it easier to run the application.

1. Running unit tests by themselves:
    make test

2. Running the whole application:
    make run

    The first thing is it stops and then removes existing containers with the same name such that it can cleanly do a docker-compose build/up.

    Then it builds the images and runs the containers via docker-compose.

    The starting point for the application is run_app.py which runs in the app_prod container.
    The other container runs the unit tests.
    The other container creates the postgres database. On spinning up it adds a new line in the pg_hba.conf of the postgres db such
    that we can connect to it from another container.
    
3. The unit tests are orchestrated in the test_orchestrator.py and it runs 2 test files called test_app.py and test_dataset_cleaner.py

4. Dataset cleaner: just an object that gives functionality to clean the pandas datasets. One can add more methods and call them on other datasets.
    To keep track of what it removes it also contains a write_to_csv method that logs what it has removed. It will contain some extra columns that
    specify which rows remain to be processed further downstream.

    For example if we run check_missing_values(columns=["col1", "col2"]) on a dataset, it will expect that there will be no missing values in 
    any of col1 and col2, otherwise it removes them and logs in the specified csv in 2 separate extra columns called no_missing_col1 and no_missing_col2.

5. App.py will just read the datasets and run some preprocessing on the datasets (like casting to numeric some columns). Then it will pass the datasets through the cleaner, add the budget/revenue ratio and upload to db.


6. For convenience, the xml has been moved to csv such that it is easier to read next times it is ran. To move xml to csv there is an option
in the Makefile called xml_to_csv so do: make xml_to_csv.

Important! I set the memory size of the containers to 8gb because reading those big files in pandas is going to crash the containers with
the default 2gb of ram. I added the memory limits in docker-compose. Alternatively, you can set them in the docker dashboard of your docker desktop.
