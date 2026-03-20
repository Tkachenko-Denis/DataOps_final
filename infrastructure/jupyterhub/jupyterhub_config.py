import os

from jupyterhub.auth import DummyAuthenticator
from jupyterhub.spawner import SimpleLocalProcessSpawner


c = get_config()

c.JupyterHub.bind_url = "http://0.0.0.0:8000"
c.JupyterHub.authenticator_class = DummyAuthenticator
c.JupyterHub.spawner_class = SimpleLocalProcessSpawner
c.Authenticator.allowed_users = {"admin"}
c.Authenticator.admin_users = {"admin"}
c.DummyAuthenticator.password = os.getenv("JUPYTERHUB_ADMIN_PASSWORD", "admin")
c.Spawner.default_url = "/lab"
c.Spawner.cmd = ["jupyterhub-singleuser"]
c.Spawner.args = ["--allow-root", "--ServerApp.ip=127.0.0.1"]
c.Spawner.ip = "127.0.0.1"
c.Spawner.notebook_dir = "/srv/jupyterhub/notebooks"
c.Spawner.http_timeout = 120
c.Spawner.start_timeout = 120
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
