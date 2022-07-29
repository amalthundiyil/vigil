import logging
import os

from sauron.backend.server import create_app
from sauron import ROOT_SAURON_DIRECTORY

# fmt = "%(asctime)s T%(thread)d %(levelname)s %(name)s [%(filename)s:%(lineno)d] - %(message)s"
# logging.basicConfig(filename=os.path.join(ROOT_SAURON_DIRECTORY, "logs", "server.log"), filemode='a', format=fmt)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
