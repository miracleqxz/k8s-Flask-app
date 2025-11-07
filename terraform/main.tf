# Main Terraform configuration
# Movie Database Application - Full Stack

# This configuration deploys a complete microservices application
# with the following components:
# - PostgreSQL (database)
# - Redis (caching)
# - RabbitMQ (message queue)
# - Elasticsearch (search engine)
# - MinIO (object storage)
# - Consul (service discovery)
# - Prometheus (monitoring)
# - Flask App (web application)
# - Analytics Worker (background processing)

# All resources are deployed in a single Kubernetes namespace
# with proper service discovery and LoadBalancer access