provider "kubernetes" {
  config_path = "~/.kube/config"
  # For MicroK8s
  config_context = "microk8s"
}

provider "helm" {
  kubernetes {
    config_path    = "~/.kube/config"
    config_context = "microk8s"
  }
}