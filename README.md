## Personal analytics
This repository contains the code for processing screenshots of screen time data and extracting the text and time using OCR(pytesseract). The intent is to add the ability to ingest data from more sources: e.g Garmin, MyFitnessPal etc. It assumes a mac development environment and local running only.
<br>

For more details see the blog post [here](https://karendavis.io/posts/01_screentime_analytics/).


## Setup Instructions
### Setup tesseract on your machine
```shell
brew install tesseract
```

### To setup a local environment
The instructions below use virtualenv to set up a local environment. The requirements.txt file contains the code dependencies. The tests/test_requirements.txt file contains the build and test dependencies: pytest, pre-commit, nbnstripout etc
```shell
cd personal-analytics
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r tests/test_requirements.txt

```
#### To setup Jupyter notebooks

```shell
source .venv/bin/activate
pip install -r notebooks/requirements.txt

```

### Git hooks
We use [pre-commit]( https://pre-commit.com) to run black for code formatting and linting and pytest unit tests before
commiting code


#### Precommit
Install the requirements under test_requirements.txt into your environment(if not already done before) and set pre-commit using the instructions below:
```shell
source .venv/bin/activate
pip install -r tests/test_requirements.txt
pre-commit install

```
To manually run use

```shell
pre-commit run --all-files
```
Otherwise they will run on git commit command

#### NBStripout
This removes output from jupyter notebooks before checking in to git.
The nbstripout package is also included in the test_requirements.txt file. To setup we run:

```shell
nbstripout --install
```

If you want to see that this has been set up successfully as a filter use
```shell
cat .git/config
```
to see the filter config    |    and
```shell
cat .git/info/attributes
```
to see the filter associated with .ipynb and .zpln files


## Run the code
### Set up the environment variables
Copy the .env.example file and rename it to .env
There are two parameters in this file that need to be updated:
1. The iCloud folder where the screenshots are stored. This project assumes that the iCloud folder you have stored the screenshots in is accessible via the macbook(i.e you are logged in with the same apple account).
```ICLOUD_FOLDER="/Users/{username}/Library/Mobile Documents/iCloud~is~workflow~my~workflows/Documents"``` Update the {username} as appropriate
2. The ```APP_LIST``` parameter. The dataloader class matches the applications found against the ones in this list. If an application is not listed here it won't be matched for time spent and end up in the outputted csv file

### To run the tests
Create a .env file in the tests folder with the same parameters and values as the environment variables above. To run the tests
```shell
python -m pytest tests/test_screen_time.py
```
or run from your ide

### To run the dataloader
app.py contains the main method that calls the dataloader to load the data from the iCloud folder, convert it to text using OCR and outputs a csv file to ```data/screen_time_data.csv```. It runs in batch mode and processes all the images in the folder each time it runs
```shell
python app.py
```
The csv file should now be generated in data/screen_time_data.csv with the following headings

|   day    |      month |       year |     total_hour |      total_min |   application_name_0    |    application_hour_0 | application_min_0 | application_name_1     |     application_hour_1 | application_min_1 | application_name_2     |     application_hour_2 |        application_min_2 |
|   ---    |-----------:|-----------:|---------------:|---------------:|:-----------------------:|----------------------:|------------------:|:-----------------------|-----------------------:|------------------:|:-----------------------|-----------------------:|-------------------------:|
|    1     |          1 |       2024 |              1 |             50 |         Safari          |                     0 |                45 |Netflix                 |                      0 |                40 | Gmail                  |                      0 |                       25 |



### To visualise the data with jupyter notebook
#### Setup the ipykernel
(Assuming the jupyter notebook dependencies have already been added to the .venv as per instructions above)
```shell
source .venv/bin/activate
python -m ipykernel install --name personal-analytics
```
#### Run the notebooks
```shell
jupyter notebook --notebook-dir notebooks
```
