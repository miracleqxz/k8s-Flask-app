output "namespace" {
  description = "Main application namespace"
  value       = kubernetes_namespace.service_checker.metadata[0].name
}

output "metallb_ip_range" {
  description = "MetalLB IP address range"
  value       = var.metallb_ip_range
}

output "argocd_server" {
  description = "ArgoCD server URL"
  value       = var.enable_argocd ? module.argocd[0].server_url : "ArgoCD not enabled"
}

output "argocd_admin_password" {
  description = "ArgoCD admin initial password"
  value       = var.enable_argocd ? module.argocd[0].admin_password : "ArgoCD not enabled"
  sensitive   = true
}