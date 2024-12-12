### Getting Started ###

First, install Conda ([Miniconda](https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html) installer works just fine).\
Then create an environment (this will install python, pip, and poetry):

    conda env create --name environment --file environment.yml

Activate the environment:

    conda activate environment

### How to configure the local setup?
Install dependencies using poetry

    POETRY_VIRTUALENVS_IN_PROJECT=true poetry install

### Start

    poetry run python app/main.py 
