# Using Patch Starter Script

Patch Starter Script is a tool to enable admins to create patch title definitions and version data to use with the Patch Server API.

The `patchstarter.py` script is available on [GitHub](https://github.com/brysontyrrell/Patch-Starter-Script). Refer to the `README` on the project's homepage for more information on usage and options.

## Create a New Title

Here is a basic example of using `patchstarter.py` to generate a definition and then sending it to the patch server:

```shell script
curl http://localhost:5000/api/v1/title \
    -X POST \
    -d "$(python patchstarter.py /Applications/GitHub\ Desktop.app -p "GitHub" )" \
    -H 'Content-Type: application/json'
```

## Update an Existing Title's Version

Here is a basic example of using `patchstarter.py` to generate version data for an application and then add it to an existing title on the patch server:

```shell script
    curl http://localhost:5000/api/v1/title/GitHubDesktop/version \
        -X POST \
        -d "$(python patchstarter.py /Applications/GitHub\ Desktop.app -p "GitHub" --patch-only)" \
        -H 'Content-Type: application/json'
```
