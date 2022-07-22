<p align='center'>
<img width="50%" src='./docs/images/logo.png'>
</p>

<h1>
<p align='center'>
Sauron - OSS Security Inspector
</p>
</h1>

<p align='center'>
<img src="https://github.com/amal-thundiyil/sauron/actions/workflows/actions.yml/badge.svg">
<a href="https://github.com/amal-thundiyil/sauron/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg">
<a href="https://github.com/amal-thundiyil/sauron/pulls"><img src="https://img.shields.io/badge/PR-Welcome-brightgreen.svg"></a>
<img src="https://visitor-badge.laobi.icu/badge?page_id=amal-thundiyil.sauron">
</p>

"_One tool to rule them all, one tool to find them, One tool to bring them all, and in the darkness bind them._"

## Introduction

This is a Swiss Army knife for DevSecOps engineers, and also normal people 🙃.

## Installation

### From Source Code

You must have Python and Docker installed to run this project.

From the project root folder run the following commands:

1. Setup the virtual environment:

```sh
python3.8 -m venv venv
source venv/bin/activate
```

2. Install the developer dependencies:

```sh
make install-dev
```

3. Start the backend:

```sh
make backend-start
```

4. Start the frontend:

```sh
make frontend-start
```

## Usage

### Sauron CLI

```console
$ sauron --help
Usage: sauron [OPTIONS] COMMAND [ARGS]...

Options:
  --version      Show version information and exit.
  -v, --verbose  Repeat for more verbosity
  --help         Show this message and exit.

Commands:
  check  Command to run any or all of the checks and scans.
  db     Command to manage the database
```
