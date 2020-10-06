# Docker Usage

## Build Image

In the `docker` directory of the project repository is a `Dockerfile` that can be used to launch the patch server as a container.

Clone the project repository to your computer. Create the Docker image with:

```shell script
% cd /path/to/PatchServer
% docker build --tag patchserver:latest -f docker/Dockerfile .
```

## Run Container

Run a container with the following command:

```shell script
% docker run -v /<patchserver-data>:/var/lib/patchserver -p 5000:5000 patchserver
```

> :information_source: Use the `-d` option to run the container in the background.

> :information_source: The `-v /<patchserver-data>:/var/lib/patchserver` option is to mount a local directory to the path in the running container where the persistent data for the patch server is stored (i.e. the database).

> :warning: If you do not attach a volume to `/var/lib/patchserver` the database will be erased when the container is stopped and removed.

You will be able to access the application using the IP address of the host (your computer's IP address when running Docker locally) at port `5000`.

## Configuration

### Enable Proxy Support

When running Patch Server behind a reverse proxy for TLS (e.g. Nginx, Apache) redirects may send a client from `https` to `http`. If your proxy is configured to pass the `X-Forwarded-For` and `X-Forwarded-Proto` headers you can enable proxy on Patch Server via environment variable.

```shell script
ENABLE_PROXY_SUPPORT=True
```

> :information_source: Use the `-e` option to pass env vars to the `docker run` command.

> :information_source: See [Proxy Setups](https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/#deploying-proxy-setups) in the Deploying Flask documentation for more details.

## Performance

The application, by default, runs 2 worker per available CPU plus 1 (a 2 CPU host will produce 5 workers) with 1 thread per worker.

## Advanced Usage

Coming soon.
