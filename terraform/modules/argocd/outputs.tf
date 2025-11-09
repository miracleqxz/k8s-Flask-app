output "namespace" {
  description = "ArgoCD namespace"
  value       = kubernetes_namespace.argocd.metadata[0].name
}

output "server_url" {
  description = "ArgoCD server URL"
  value       = "Get from: kubectl get svc argocd-server -n argocd"
}

output "admin_password" {
  description = "ArgoCD admin password"
  value       = try(data.kubernetes_secret.argocd_initial_admin_secret.data["password"], "")
  sensitive   = true
}