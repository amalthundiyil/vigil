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
<a href="https://github.com/amal-thundiyil/sauron/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg"></a>
<img src="https://visitor-badge.laobi.icu/badge?page_id=amal-thundiyil.sauron">
</p>

> "_One tool to rule them all, one tool to find them, One tool to bring them all, and in the darkness bind them._"

## Introduction

Sauron is an easy way for consumers of open-source projects to judge whether their dependencies are really safe.

It is an automated tool that assesses a number of important heuristics associated with software security and assigns each check a score. You can use these scores to understand specific areas to improve in order to strengthen the security posture of your project. You can also assess the risks that dependencies introduce, and make informed decisions about accepting these risks, evaluating alternative solutions, or working with the maintainers to make improvements.

## Installation

### From Source Code

> 💡 You will need Python, Node and Docker to run the project successfully. You can install it simply by running:
>
> ```sh
> sudo apt install python3.8 python3.8-dev python3.8-venv python3-pip nodejs npm
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

```sh
$ sauron check --url "https://github.com/amal-thundiyil/moni-moni" 

███████╗ █████╗ ██╗   ██╗██████╗  ██████╗ ███╗   ██╗
██╔════╝██╔══██╗██║   ██║██╔══██╗██╔═══██╗████╗  ██║
███████╗███████║██║   ██║██████╔╝██║   ██║██╔██╗ ██║
╚════██║██╔══██║██║   ██║██╔══██╗██║   ██║██║╚██╗██║
███████║██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

🧐 Running all checks
🌏  Analyzing community
✔️  Completed community analysis
📈️  Analyzing popularity
✔️  Completed popularity analysis
🛠️  Analyzing maintainence
✔️  Completed maintainence analysis
🛡️  Analyzing security
✔️  Completed security analysis


╒══════════════╤═════════╤══════════════════════════════════════════════════════╕
│ Metrics      │   Score │ Description                                          │
╞══════════════╪═════════╪══════════════════════════════════════════════════════╡
│ Community    │    2.37 │ Community is active and has a strong code of conduct │
├──────────────┼─────────┼──────────────────────────────────────────────────────┤
│ Popularity   │    0.57 │ Repo is popular and downloaded frequently            │
├──────────────┼─────────┼──────────────────────────────────────────────────────┤
│ Maintainence │    3.39 │ Repo is well maintained and has active maintainers   │
├──────────────┼─────────┼──────────────────────────────────────────────────────┤
│ Security     │    5.3  │ Repo is secure with few problems                     │
╘══════════════╧═════════╧══════════════════════════════════════════════════════╛


🚩 Aggregate score: 2.91
📜 Aggregate summary: Got score of 2.91
```
