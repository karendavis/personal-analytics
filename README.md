
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

##### Precommit
Install the requirements under test_requirements.txt into your environment and set pre-commit using the instructions below:
```shell
pip install -r tests/test_requirements.txt
pre-commit install

```
To manually run use

```shell
pre-commit run --all-files
```
Otherwise they will run on git commit command

##### NBStripout
This removes output from jupyter notebooks before checking in to git.
The nbstripout package is also included in the test_requirements.txt file. To setup we run:

```shell
nbstripout --install
```

If you want to see that this has been set up successfully as a filter use
```shell
cat .git/config
```
to see the filter config, and
```shell
cat .git/info/attributes
```
to see the filter associated with .ipynb and .zpln files
