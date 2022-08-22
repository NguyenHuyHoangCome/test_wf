resource "kubernetes_deployment" "msa-sms" {

  metadata {
    name = "msa-sms"
    labels = {
      service = "msa-sms"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "msa-sms"
      }
    }
    strategy {
      type = "Recreate"
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "msa-sms"
        }
      }
      spec {
        container {
          image = var.msa2_sms_img
          name  = "msa-sms"
          port {
            container_port = 28165
          }
          port {
            container_port = 28169
          }
          port {
            container_port = 3690
          }
          port {
            container_port = 28172
          }
          security_context {
            capabilities {
              add = ["NET_ADMIN"]
            }
            privileged = true
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
            mount_path = "/opt/sms/logs"
            name       = "msa-sms-logs"
          }
          volume_mount {
            mount_path = "/opt/svnroot"
            name       = "msa-svn"
          }
          liveness_probe {
            exec {
              command = ["/etc/init.d/ubi-sms status | grep -q 'service seems UP' || exit 1"]
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
          name = "msa-sms-logs"
          persistent_volume_claim {
            claim_name = "msa-sms-logs"
          }
        }
        volume {
          name = "msa-svn"
          persistent_volume_claim {
            claim_name = "msa-svn"
          }
        }
      }
    }
  }
}
