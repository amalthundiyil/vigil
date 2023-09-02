import logging
import os

from vigil.backend.server import create_app
from vigil import ROOT_VIGIL_DIRECTORY

# fmt = "%(asctime)s T%(thread)d %(levelname)s %(name)s [%(filename)s:%(lineno)d] - %(message)s"
# logging.basicConfig(filename=os.path.join(ROOT_VIGIL_DIRECTORY, "logs", "server.log"), filemode='a', format=fmt)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
