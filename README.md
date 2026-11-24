# End-to-End MLOps Kubernetes Deployment

## Workflow
`Terraform -> Minikube -> Jenkins -> MLflow -> Kubernetes (3 Replicas) -> Nginx Ingress Load Balancer`

## Project Structure
- `infra/`: Terraform configuration for Minikube Kubernetes cluster (`mlops-cluster`) with Nginx Ingress.
- `pipeline/`: Kubeflow pipeline definition (`iris_pipeline.py` & compiled `iris_pipeline.yaml`) and MLflow model training/registry script (`train_and_register.py`).
- `k8s/`: Kubernetes Deployment (3 replicas), ClusterIP Service, and Nginx Ingress manifest (`deployment.yaml`).
- `Jenkinsfile`: CI/CD automation pipeline for compiling, training, registering, and deploying the model.
