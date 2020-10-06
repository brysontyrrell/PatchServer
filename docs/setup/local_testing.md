# Local Testing

> :warning:  Though you can run the application locally using `run.py` it is **strongly** recommended you perform testing with Docker (use the same image you would deploy in production). See the [Docker setup documentation](docker.md) to learn more.

Clone the project repository to the system that will run the application.

Change into the directory for the project, create a Python virtual environment, and install the project dependencies using `pipenv`. Then use `run.py` to start the app.

```shell script
% cd /path/to/PatchServer
% pipenv install --deploy
% pipenv run python run.py
```

You will be able to access the application using `localhost` or your computer's IP address at port `5000`.

The Patch Server database file will default to `patchserver/patch_server.db` in the repository. You can change the location of this file by setting the `DATABASE_DIR` environment variable.
