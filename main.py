from config.conf import HTTP_PORT
from server import app

if __name__ == "__main__":
    app.app.run(port=HTTP_PORT)
