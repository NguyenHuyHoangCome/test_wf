resource "kubernetes_deployment" "msa-dev" {

  metadata {
    name = "msa-dev"
    labels = {
      service = "msa-dev"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "msa-dev"
      }
    }
    strategy {
      type = "Recreate"
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "msa-dev"
        }
      }
      spec {
        container {
          image = var.msa2_dev_img
          name  = "msa-dev"
          port {
            container_port = 22
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
      }
    }
  }
}
