# Django API

## Features

* Builds and deploys to Kubernetes / Rancher
* Comes with a baseline of tests

## Notable Libraries
| Name | Version |
|:----:|:-------:|
| Django | 3.0.5 |
| Django Allauth | 0.41.0 |
| Django Rest Framework | 3.11.0 |
| drf-yasg (Swagger) | 1.17.1 |
| Gunicorn | 20.0.4 |

## Log in

After launching the server go to http://localhost:8000/ and log in with user `admin`, password `admin`.

## During Development

Any changes in your code will be reflected in the `/build` directory on the app container through a mount.

To run tests:

    docker-compose run --rm --no-deps app pytest

To drop into a shell on the app container, run:

    docker-compose run --rm app /bin/ash

You can execute Django management commands with the `manage-compose.py` helper script:

    python3 manage-compose.py shell

If you want to revert to the initial state during development, run the entrypoint
with the `--recreate` flag:

    python3 manage-compose.py db_entrypoint --recreate

Install new packages:

    docker-compose run --rm app pip3 install --upgrade Django

If you want to see the logs of the cluster you need to run:

    docker-compose logs -f --tail=100 app

To search for logs in the output use:

    docker-compose logs -f --tail=100 app 2>&1 | grep "500"

In order to stop and remove the cluster you need to run:

    docker-compose down

Upgrading dependencies:

    pip install piprot
    # This will only output the new requirements.txt and requirements-devel.txt combined
    # Add the output to the files by splitting them
    piprot --latest --verbatim requirements-devel.txt

Because most of these commands are quite long, help yourself by searching through your shell's
history with `Ctrl+R` and for example `build`.

## Setting up PyCharm

1. [Build and launch the services](#launching-services-in-docker) in your terminal
1. Add a [Remote Project Interpreter with Docker Compose](https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html)
    1. Set the Python interpreter path to `python3`
1. Back in the Project Interpreter screen, set the Path mapping from your project root directory
   to the remote path `/build`
1. Close the settings screen
1. While keeping all containers running in your terminal, launch one of the run configurations in PyCharm.
   The running app instance will be stopped and replaced by one that PyCharm has patched
   with helper functions for code completion, debugging, etc.

## Documentation and Tests

API documentation is automatically generated for Swagger.
Add doc-blocks in your API views and check the results on
- Swagger: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

Exports are also available
- YAML: http://localhost:8000/api/docs/swagger.yaml
- JSON: http://localhost:8000/api/docs/swagger.yaml

Tests should be added in a `tests` package in each app, or in the root `tests` package
for generic test cases.

Non-app-specific helper functions and classes should be added in the root `libs` package.

## Kubernetes
For local development we recommend [Minikube](https://minikube.sigs.k8s.io/docs/start/)
1. Start the local Kubernetes Instance
```
    minikube start
```
2. Enable the registry: [Documentation](https://minikube.sigs.k8s.io/docs/handbook/registry/)
```
    minikube addons enable registry
```
4. Forward the internal port of the registry to 127.0.0.1:5000 (Needs to stay open)
```
   kubectl port-forward -n kube-system replicationcontroller/registry 5000:5000
```
5. Enable the ingress
```
    minikube addons enable ingress
```
6. Optional: Patch hosts file to access via browser
```
    echo $(minikube ip) django-kompose.minikube.local django-kustomize.minikube.local django-helm.minikube.local | sudo tee -a /etc/hosts
```

### Using Kompose

Conversion using environment defined in .env
```
    cd k8s/kompose
    docker-compose config | kompose convert --stdout -f - | kubectl apply -f -
```

Access: http://django-kompose.minikube.local

### Using Kustomize

This repo contains a simple manifest for this application in `k8s/kustomize/base`
There are two overlays available that you can have a look at
1. Minikube (Access: http://django-kustomize.minikube.local)
```
    cd k8s/kustomize
    kubectl apply -k overlays/minikube/
```
2. Production
```
    cd k8s/kustomize
    kubectl apply -k overlays/production/
```

### Using helm (with helmfile)

This repo also contains a simple Helm chart for the application in `k8s/helm/django`
To start it either use helm directly or run it using helmfile

```
    cd k8s/helmfile
    helmfile apply
```

Access: http://django-helm.minikube.local

### Using Skaffold

On top of the three options there is also an option to use skaffold
```
    skaffold dev --port-forward
```