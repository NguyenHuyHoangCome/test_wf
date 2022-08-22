resource "kubernetes_deployment" "msa-alarm" {

  metadata {
    name = "msa-alarm"
    labels = {
      service = "msa-alarm"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "msa-alarm"
      }
    }
    strategy {
      type = "Recreate"
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "msa-alarm"
        }
      }
      spec {
        container {
          image = var.msa2_alarm_img
          name  = "msa-alarm"
          env {
            name  = "ES_CREDENTIALS"
            value = "c3VwZXJ1c2VyOnheWnl1R002fnU9K2ZZMkc="
          }
          port {
            container_port = 28164
          }
          liveness_probe {
            exec {
              command = ["/etc/init.d/ubi-alarm status | grep -q 'service seems UP' || exit 1"]
            }
          }
          volume_mount {
            mount_path = "/opt/sms/logs"
            name       = "msa-sms-logs"
          }
        }
        restart_policy = "Always"
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
