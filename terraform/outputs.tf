output "namespace" {
  description = "Kubernetes namespace"
  value       = kubernetes_namespace.service_checker.metadata[0].name
}

output "flask_app_url" {
  description = "Flask application URL (LoadBalancer)"
  value       = "http://${kubernetes_service.flask_app.status[0].load_balancer[0].ingress[0].ip}"
}

output "postgres_host" {
  description = "PostgreSQL service host"
  value       = "${kubernetes_service.postgres.metadata[0].name}.${var.namespace}.svc.cluster.local"
}

output "redis_host" {
  description = "Redis service host"
  value       = "${kubernetes_service.redis.metadata[0].name}.${var.namespace}.svc.cluster.local"
}

output "elasticsearch_host" {
  description = "Elasticsearch service host"
  value       = "${kubernetes_service.elasticsearch.metadata[0].name}.${var.namespace}.svc.cluster.local"
}

output "minio_console_url" {
  description = "MinIO console URL"
  value       = "http://${kubernetes_service.minio.status[0].load_balancer[0].ingress[0].ip}:9001"
}

output "rabbitmq_management_url" {
  description = "RabbitMQ management UI URL"
  value       = "http://${kubernetes_service.rabbitmq.status[0].load_balancer[0].ingress[0].ip}:15672"
}

output "prometheus_url" {
  description = "Prometheus UI URL"
  value       = "http://${kubernetes_service.prometheus.status[0].load_balancer[0].ingress[0].ip}:9090"
}