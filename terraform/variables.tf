

variable "namespace" {
  description = "Kubernetes namespace for the project"
  type        = string
  default     = "service-checker"
}

variable "flask_image" {
  description = "Flask application Docker image"
  type        = string
  default     = "ghcr.io/miracleqxz/k8s-flask-app:latest"
}

variable "flask_replicas" {
  description = "Number of Flask app replicas"
  type        = number
  default     = 2
}

variable "postgres_image" {
  description = "PostgreSQL Docker image"
  type        = string
  default     = "postgres:16"
}

variable "redis_image" {
  description = "Redis Docker image"
  type        = string
  default     = "redis:7-alpine"
}

variable "rabbitmq_image" {
  description = "RabbitMQ Docker image"
  type        = string
  default     = "rabbitmq:3.12-management"
}

variable "elasticsearch_image" {
  description = "Elasticsearch Docker image"
  type        = string
  default     = "docker.elastic.co/elasticsearch/elasticsearch:8.11.0"
}

variable "minio_image" {
  description = "MinIO Docker image"
  type        = string
  default     = "minio/minio:latest"
}

variable "consul_image" {
  description = "Consul Docker image"
  type        = string
  default     = "consul:1.17"
}

variable "prometheus_image" {
  description = "Prometheus Docker image"
  type        = string
  default     = "prom/prometheus:v2.48.0"
}

variable "postgres_password" {
  description = "PostgreSQL password"
  type        = string
  default     = "postgres"
  sensitive   = true
}

variable "rabbitmq_user" {
  description = "RabbitMQ username"
  type        = string
  default     = "guest"
}

variable "rabbitmq_password" {
  description = "RabbitMQ password"
  type        = string
  default     = "guest"
  sensitive   = true
}

variable "minio_access_key" {
  description = "MinIO access key"
  type        = string
  default     = "minioadmin"
  sensitive   = true
}

variable "minio_secret_key" {
  description = "MinIO secret key"
  type        = string
  default     = "minioadmin"
  sensitive   = true
}