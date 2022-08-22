resource "kubernetes_deployment" "msa-monitoring" {

  metadata {
    name = "msa-monitoring"
    labels = {
      service = "msa-monitoring"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "msa-monitoring"
      }
    }
    strategy {
      type = "Recreate"
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "msa-monitoring"
        }
      }
      spec {
        container {
          image = var.msa2_monitoring_img
          name  = "msa-monitoring"
          port {
            container_port = 162
          }
          env {
            name  = "ES_CREDENTIALS"
            value = "c3VwZXJ1c2VyOnheWnl1R002fnU9K2ZZMkc="
          }
          volume_mount {
            mount_path = "/opt/devops/"
            name       = "msa-dev"
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
            mount_path = "/opt/sms/spool/parser"
            name       = "msa-bulkfiles"
          }
          volume_mount {
            mount_path = "/opt/sms/logs"
            name       = "msa-sms-logs"
          }
          liveness_probe {
            exec {
              command = ["/etc/init.d/ubi-poll status | grep -q 'service seems UP' || exit 1"]
            }
          }
        }
        restart_policy = "Always"
        volume {
          name = "msa-dev"
          persistent_volume_claim {
            claim_name = "msa-dev"
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
          name = "msa-bulkfiles"
          persistent_volume_claim {
            claim_name = "msa-bulkfiles"
          }
        }
        volume {
          name = "msa-sms-logs"
          persistent_volume_claim {
            claim_name = "msa-sms-logs"
          }
        }
      }
    }
  }
}
