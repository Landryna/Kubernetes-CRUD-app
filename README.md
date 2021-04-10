# Kubernetes-CRUD-app
"K8S Crud app" is application created in Python used to serve REST API which communicates with Kubernetes API server.
Operations are available for Pod,Service,Namespace objects but app is pretty much easy to expand if more K8s objects are needed to modify.

Application serves SwaggerUI which is popular UI available on the client's browser side.
Whole deployment of application is automated in bash script.
Script is resposbile for running unit tests against application. If test pass application is deployed on cluster as
Helm release.
