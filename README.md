The datasets we will refer to throughout the exercise:
    https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz
    https://www.kaggle.com/rounakbanik/the-movies-dataset/version/7#movies_metadata.csv


In the exercise it mentions nothing is installed, but I hope it is ok if I take for granted 
tools like docker and python3 as being installed. If not: 
    docker: https://docs.docker.com/desktop/mac/install/
    python3: https://www.python.org/downloads/macos/ (or use brew and type: brew install python)
    pip comes with python
    libraries will be installed via requirements.txt by docker
    CMake: https://cmake.org/install/ (or use brew and type: brew install cmake)

I use CMake to make it easier to run the application. It allows you to type make <SOMEOPTION> and it runs
the specific option. Throughout this application I have in the Makefile: .PHONY: run, test, xml_to_csv to define my makefile
options.


IMPORTANT!
Loading all the data in git is not best practice and it is too big to do so. Therefore:
    Create 2 folders at the root of the repo called data_imdb and data_wikipedia. Unzip the datasets there.
    Hence, the root should look like:

        truelayer
            app/
            data_imdb/
                here unzip imdb data
            data_wikipedia/
                here unzip wikipedia data
            .gitignore
            truelayer_db/
            docker-compose.yml
            LICENSE
            Makefile
            README.md

1. For convenience, the xml is moved to csv such that it is easier to read next times it is ran. To move xml to csv there is an option
in the Makefile called xml_to_csv so type in the terminal: 
    make xml_to_csv

    This code will load the xml into memory and then write it on disk as a csv. Because it is a massive xml file, it will take a while.
    On my laptop it runs for 15minutes.

    This step is needed because the app.py will read from the newly created csv rather than xml.

2. Running the whole application:
    make run

    The first thing is it stops and then removes existing containers with the same name such that it can cleanly do a docker-compose build/up.

    Then it builds the images and runs the containers via docker-compose.

    The starting point for the application is run_app.py which runs in the app_prod container.
    The other container runs the unit tests.
    The other container creates the postgres database. On spinning up it adds a new line in the pg_hba.conf of the postgres db such
    that we can connect to it from another container.

6. As mentioned above, the app_prod docker service will run run_app.py. It will just read the datasets and run some preprocessing on the datasets (like casting to numeric some columns). Then it will pass the datasets through a dataset cleaner (see number 5), add the budget/revenue ratio and upload to db.

3. Running unit tests by themselves:
    make test

    However they also run as part of the make run

4. The unit tests are orchestrated in the test_orchestrator.py and it runs 2 test files called test_app.py and test_dataset_cleaner.py

5. Dataset cleaner: just an object that gives functionality to clean the pandas datasets. One can add more methods and call them on other datasets.
    To keep track of what it removes it also contains a write_to_csv method that logs what it has removed. It will contain some extra columns that
    specify which rows remain to be processed further downstream.

    For example if we run check_missing_values(columns=["col1", "col2"]) on a dataset, it will expect that there will be no missing values in 
    any of col1 and col2, otherwise it removes them and logs in the specified csv in 2 separate extra columns called no_missing_col1 and no_missing_col2.






Important! I set the memory size of the containers to 8gb because reading those big files in pandas is going to crash the containers with
the default 2gb of ram. I added the memory limits in docker-compose. Alternatively, you can set them in the docker dashboard of your docker desktop.
