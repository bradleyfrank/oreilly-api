# Mock Up Flask API Endpoint

Mock up API endpoint using O'Reilly API.

## Setup

Secrets and passwords don't _really_ matter in this instance. Generate a `.env` (for Docker) and a `secrets.yaml` (for K8s) by running:

    sh env.sh

### Docker

To get started with Docker, run:

    docker-compose up -d

And connect to http://localhost.

### Kubernetes

To get started with Kubernetes, run:

    kubectl apply -f k8s-secrets.yml
    kubectl apply -f k8s-services.yml
    kubectl apply -f k8s-deployments.yml

Get the NodePort:

    kubectl get service oreilly-api --no-headers -o custom-columns="PORT:.spec.ports[*].nodePort"

And connect to http://localhost:{NodePort}

*Tested on Docker Desktop Kubernetes 1.16.*