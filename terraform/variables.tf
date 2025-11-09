variable "namespace" {
  description = "Main application namespace"
  type        = string
  default     = "service-checker"
}

variable "metallb_ip_range" {
  description = "IP range for MetalLB"
  type        = string
  default     = "127.0.0.1-127.0.0.20"
}

variable "enable_argocd" {
  description = "Enable ArgoCD installation"
  type        = bool
  default     = true
}

variable "enable_monitoring" {
  description = "Enable monitoring stack (Prometheus, Grafana)"
  type        = bool
  default     = true
}

variable "argocd_version" {
  description = "ArgoCD Helm chart version"
  type        = string
  default     = "5.51.4"
}

variable "github_repo_url" {
  description = "GitHub repository URL for ArgoCD"
  type        = string
  default     = "https://github.com/miracleqxz/k8s-Flask-app.git"
}

variable "telegram_bot_token" {
  description = "Telegram bot token (sensitive)"
  type        = string
  sensitive   = true
  default     = ""
}

variable "telegram_chat_id" {
  description = "Telegram chat ID"
  type        = string
  sensitive   = true
  default     = ""
}