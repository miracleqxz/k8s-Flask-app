resource "kubernetes_namespace" "service_checker" {
  metadata {
    name = var.namespace

    labels = {
      name        = var.namespace
      managed-by  = "terraform"
      environment = "production"
    }
  }
}


resource "kubernetes_secret" "telegram_bot" {
  metadata {
    name      = "telegram-bot"
    namespace = kubernetes_namespace.service_checker.metadata[0].name
  }

  data = {
    bot-token = var.telegram_bot_token
    chat-id   = var.telegram_chat_id
  }

  type = "Opaque"
}

# MetalLB IP Address Pool
resource "kubernetes_config_map" "metallb_config" {
  metadata {
    name      = "config"
    namespace = "metallb-system"
  }

  data = {
    config = <<-EOT
      address-pools:
      - name: default
        protocol: layer2
        addresses:
        - ${var.metallb_ip_range}
    EOT
  }

  depends_on = [
    null_resource.enable_metallb
  ]
}


resource "null_resource" "enable_metallb" {
  provisioner "local-exec" {
    command = "microk8s enable metallb:${var.metallb_ip_range}"
  }

  # Only run once
  triggers = {
    ip_range = var.metallb_ip_range
  }
}

resource "null_resource" "enable_dns" {
  provisioner "local-exec" {
    command = "microk8s enable dns"
  }
}

resource "null_resource" "enable_storage" {
  provisioner "local-exec" {
    command = "microk8s enable hostpath-storage"
  }
}

resource "null_resource" "enable_helm" {
  provisioner "local-exec" {
    command = "microk8s enable helm3"
  }
}

module "argocd" {
  source = "./modules/argocd"
  count  = var.enable_argocd ? 1 : 0

  argocd_version  = var.argocd_version
  github_repo_url = var.github_repo_url

  depends_on = [
    kubernetes_namespace.service_checker
  ]
}