# Installation

> 💡 You will need Python, Node and Docker to run the project successfully. You can install it simply by running:
>
> ```sh
> sudo apt install python3.8 python3.8-dev python3.8-venv python3-pip nodejs npm
> ```

From the project root folder run the following commands:

1. Setup a virtual environment to run the project in:

```sh
python3.8 -m venv venv
source venv/bin/activate
```

2. If you are going to use Elasticsearch (required for Web UI) then run the following command:

```sh
sudo sysctl -w vm.max_map_count=262144
docker-compose up
```

3. Install the developer dependencies:

```sh
make install-dev
```

3. Start the backend Flask server

```sh
make backend-start
```

4. Start the frontend React application

```sh
make frontend-start
```

Setup the `vigil.config.json` configuration file with the configuration values. You can refer to `vigil.example.json` for details.
