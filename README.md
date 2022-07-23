<p align='center'>
<img width="40%" src='./docs/images/logo.png'>
</p>

<h1>
<p align='center'>
Sauron - OSS Security Inspector
</p>
</h1>

<p align='center'>
<img src="https://github.com/amal-thundiyil/sauron/actions/workflows/actions.yml/badge.svg">
<a href="https://github.com/amal-thundiyil/sauron/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg">
<img src="https://visitor-badge.laobi.icu/badge?page_id=amal-thundiyil.sauron">
</p>

> "_One tool to rule them all, one tool to find them, One tool to bring them all, and in the darkness bind them._"

## Introduction

TL;DR - Sauron is a Swiss Army knife for DevSecOps engineers, and also normal people 🙃.

## Installation

### From Source Code

> You will need python3-pip, nodejs, npm and Docker to run the project successfully. You can install it simply by running:
>
> ```sh
> sudo apt install python3-pip python3.8-dev python3.8-venv nodejs npm
> ```

From the project root folder run the following commands:

```sh
# setup the virtual environment
python3.8 -m venv venv
source venv/bin/activate

# install the developer dependencies:
make install-dev

# start the backend:
make backend-start

# start the frontend:
make frontend-start
```

Setup the `sauron.config.json` configuration file with the desired configuration values.

## Usage

### Sauron CLI

```console
$ sauron --help
Usage: sauron [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show version information and exit.
  --help     Show this message and exit.

Commands:
  check  Run different all (default) or specified checks
  db     Command to manage the database
```
