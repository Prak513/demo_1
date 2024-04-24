#### Prerequisites: Docker, Kubernetes cluster

 


### Steps:

1. Build the docker image with name `demo` from Dockerfile : `docker build --tag demo .`
2. In `kubectl` command line run `kubectl apply -f flask.yaml`
3. Make curl request as `curl localhost:30007/info` & get response as `["topic-1", "topic-2"]`