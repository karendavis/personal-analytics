
### To setup a local environment
I used virtualenv to set up a local environment
```shell
cd personal-analytics
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r tests/test_requirements.txt

```





### Git hooks
I'm using [pre-commit]( https://pre-commit.com) to run black for code formatting and linting, pytest unit tests before
commiting code

#### To setup:

Install the requirements under test_requirements.txt into your environment and set pre-commit using the instructions below:
```shell
pip install -r tests/test_requirements.txt
pre-commit install

```
To manually run use

```shell
pre-commit run --all-files
```
Other wise they will run on git commit command
