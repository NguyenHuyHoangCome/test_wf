resource "kubernetes_deployment" "msa-api" {

  metadata {
    name = "msa-api"
    labels = {
      service = "msa-api"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "msa-api"
      }
    }
    strategy {
      type = "Recreate"
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "msa-api"
        }
      }
      spec {
        container {
          image = var.msa2_api_img
          name  = "msa-api"
          env {
            name  = "ES_CREDENTIALS"
            value = "c3VwZXJ1c2VyOnheWnl1R002fnU9K2ZZMkc="
          }
          port {
            container_port = 8480
          }
          port {
            container_port = 8787
          }
          liveness_probe {
            exec {
              command = ["curl --fail http://localhost:8480"]
            }
          }
          volume_mount {
            mount_path = "/opt/ubi-jentreprise/generated/conf"
            name       = "msa-api"
          }
          volume_mount {
            mount_path = "/opt/fmc_entities"
            name       = "msa-entities"
          }
          volume_mount {
            mount_path = "/opt/fmc_repository"
            name       = "msa-repository"
          }
          volume_mount {
            mount_path = "/opt/rrd"
            name       = "rrd-repository"
          }
          volume_mount {
            mount_path = "/opt/devops/"
            name       = "msa-dev"
          }
          volume_mount {
            mount_path = "/opt/wildfly/logs/"
            name       = "msa-api-logs"
          }
        }
        restart_policy = "Always"
        volume {
          name = "msa-api"
          persistent_volume_claim {
            claim_name = "msa-api"
          }
        }
        volume {
          name = "msa-entities"
          persistent_volume_claim {
            claim_name = "msa-entities"
          }
        }
        volume {
          name = "msa-repository"
          persistent_volume_claim {
            claim_name = "msa-repository"
          }
        }
        volume {
          name = "rrd-repository"
          persistent_volume_claim {
            claim_name = "rrd-repository"
          }
        }
        volume {
          name = "msa-dev"
          persistent_volume_claim {
            claim_name = "msa-dev"
          }
        }
        volume {
          name = "msa-api-logs"
          persistent_volume_claim {
            claim_name = "msa-api-logs"
          }
        }
      }
    }
  }
}
