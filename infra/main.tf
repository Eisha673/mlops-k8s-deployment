resource "minikube_cluster" "docker" {
  driver       = "docker"
  cluster_name = var.cluster_name
  addons       = ["ingress", "default-storageclass", "storage-provisioner"]
  cpus         = var.cpus
  memory       = var.memory
}
