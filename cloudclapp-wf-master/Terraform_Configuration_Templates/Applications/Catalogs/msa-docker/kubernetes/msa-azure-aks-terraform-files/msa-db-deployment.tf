resource "kubernetes_deployment" "db" {

  metadata {
    name = "db"
    labels = {
      service = "db"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "db"
      }
    }
    strategy {
      type = "Recreate"
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "db"
        }
      }
      spec {
        container {
          image = var.msa2_db_img
          name  = "msa-db"
          port {
            container_port = 5432
          }
          args = ["postgres", "-c", "max_connections=800", "-c", "max_prepared_transactions=100"]
          env {
            name  = "CAMUNDA_DB"
            value = "process-engine"
          }
          env {
            name  = "CAMUNDA_PASSWORD"
            value = "process-engine"
          }
          env {
            name  = "CAMUNDA_USER"
            value = "camunda"
          }
          env {
            name  = "POSTGRES_DB"
            value = "POSTGRESQL"
          }
          env {
            name  = "POSTGRES_PASSWORD"
            value = "my_db_password"
          }
          env {
            name  = "PGDATA"
            value = "/var/lib/postgresql/data"
          }
          liveness_probe {
            exec {
              command = ["pg_isready -U postgres"]
            }
            failure_threshold = 3
            period_seconds    = 30
            timeout_seconds   = 60
          }
          volume_mount {
            mount_path = "/var/lib/postgresql"
            name       = "msa-db"
          }
        }
        restart_policy = "Always"
        volume {
          name = "msa-db"
          persistent_volume_claim {
            claim_name = "msa-db"
          }
        }
      }
    }
  }
}
