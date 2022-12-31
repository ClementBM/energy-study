# Development setup
## Prerequisites
This following packages must be installed
* python
* poetry
* git

## Configuration
* `poetry` configuration, add environment variable `POETRY_VIRTUALENVS_IN_PROJECT=true`
* `vscode` configuration, add environment variable `PYTHON_VENV_LOC`
  * on windows: `PYTHON_VENV_LOC=.venv\\bin\\python.exe`
  * on linux: `PYTHON_VENV_LOC=.venv/bin/python`
* `git` configuration
```shell
git config --global user.name 'your name'
git config --global user.email 'your email'
```

## Initialization
* First setup `poetry install`
* Then `poetry shell`

# Build and publish with poetry
## Build
Manuel steps to generate and publish the package to TestPyPI with poetry, documentation from [packaging.python](https://python-poetry.org/docs/)

Build the package, generate distribution archives
```shell
poetry build
```

## Publish to Test PyPI
Add Test PyPI as an alternate package repository
```shell
poetry config repositories.testpypi https://test.pypi.org/legacy/
```

Upload/publish package/distribution archive to TestPyPI (a separate instance of the Python Package Index)
```shell
poetry publish -r testpypi
```

## Installation with pip
```shell
pip install --index-url https://test.pypi.org/simple/ energy-study
```
or
```shell
pip3 install --index-url https://test.pypi.org/simple/ energy-study
```

# Code of Conduct

# History (changelog)

## Swagger
```shell
curl -X POST -H "content-type:application/json" -d '{"swaggerUrl":"https://petstore.swagger.io/v2/swagger.json"}' https://generator.swagger.io/api/gen/clients/python
```

you can POST to https://generator.swagger.io/api/gen/clients/{language} with the following HTTP body

```json
{
  "options": {
    "packageName": "energ_study"
  },
  "spec": {

  }
}
```

### Swagger code generation
https://swagger.io/tools/swagger-codegen/
Online generator for api client

```shell
curl -X POST -H "content-type:application/json" -d '{"swaggerUrl":"https://petstore.swagger.io/v2/swagger.json"}' https://generator.swagger.io/api/gen/clients/ruby
```

https://generator.swagger.io/#/clients/generateClient

## RTE API
https://data.rte-france.com/catalog/consumption

Il est conseillé de faire un appel par heure à ce service et de ne pas dépasser une période de 155 jours par appel.


## Prediction J-1 Error

The residuals are the rescaled one-step prediction errors
$$
\hat{W_t} = (X_t - \hat{X_t}) / \sqrt{r_{t-1}}
$$

$$
r_{t-1} = E(X_t - \hat{X_t}) / \sigma^2
$$

$\sigma^2$ is the white noise variance of the fitted model

To check the appropriateness of the model we therefore examine the residual series $\hat{W_t}$, and check that it resembles a realization of a white noise sequence.

* Plot
* QQ-Plot (normal)
* QQ-Plot (t-distr)
* Histogram
* ACF/PACF
* ACF Abs vals/Squares
* Tests of randomness



* distribution
* descriptive statistics: mean, median, std, ...
* ACF and PACF
* stationarity ?


# Open Data

Données de modèle de prévision d'ensemble arpege

donneespubliques.meteofrance.fr

## ECMWF Data

```json
{
    "url"   : "https://api.ecmwf.int/v1",
    "key"   : "XXX",
    "email" : "XXX"
}
```

https://confluence.ecmwf.int/display/WEBAPI/Access+ECMWF+Public+Datasets

See Public Datasets on https://apps.ecmwf.int/datasets/

```shell
pip install ecmwf-api-client
```

```shell
sudo apt -y install libgeos-dev
```