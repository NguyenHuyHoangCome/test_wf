resource "kubernetes_deployment" "msa-bud" {

  metadata {
    name = "msa-bud"
    labels = {
      service = "msa-bud"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "msa-bud"
      }
    }
    strategy {
      type = "Recreate"
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "msa-bud"
        }
      }
      spec {
        container {
          image = var.msa2_bud_img
          name  = "msa-bud"
          port {
            container_port = 28170
          }
          liveness_probe {
            exec {
              command = ["/etc/init.d/ubi-bud status | grep -q 'service seems UP' || exit 1"]
            }

            failure_threshold = 3
            period_seconds    = 30
            timeout_seconds   = 60
          }
          volume_mount {
            mount_path = "/opt/bud/logs/"
            name       = "msa-bud-logs"
          }
        }
        restart_policy = "Always"
        volume {
          name = "msa-bud-logs"
          persistent_volume_claim {
            claim_name = "msa-bud-logs"
          }
        }
      }
    }
  }
}
