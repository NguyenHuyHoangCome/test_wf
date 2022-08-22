resource "kubernetes_deployment" "camunda" {

  metadata {
    name = "camunda"
    labels = {
      service = "camunda"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "camunda"
      }
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "camunda"
        }
      }
      spec {
        container {
          image = var.msa2_camunda_img
          name  = "msa-camunda"
          port {
            container_port = 8080
          }
          env {
            name  = "DB_DRIVER"
            value = "org.postgresql.Driver"
          }
          env {
            name  = "DB_PASSWORD"
            value = "camunda"
          }
          env {
            name  = "DB_URL"
            value = "jdbc:postgresql://db:5432/process-engine"
          }
          env {
            name  = "DB_USERNAME"
            value = "camunda"
          }
          env {
            name  = "DB_VALIDATE_ON_BORROW"
            value = "true"
          }
          env {
            name  = "WAIT_FOR"
            value = "db:5432"
          }
          env {
            name  = "WAIT_FOR_TIMEOUT"
            value = "60"
          }
        }
        restart_policy = "Always"
      }
    }
  }
}
