resource "kubernetes_deployment" "msa-ai-ml" {

  metadata {
    name = "msa-ai-ml"
    labels = {
      service = "msa-ai-ml"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "msa-ai-ml"
      }
    }
    strategy {
      type = "Recreate"
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "msa-ai-ml"
        }
      }
      spec {
        container {
          image = var.msa2_ai_ml_img
          name  = "msa-ai-ml"
          port {
            container_port = 8000
          }
          liveness_probe {
            exec {
              command = ["python /msa_proj/health_check.py"]
            }
          }
          volume_mount {
            mount_path = "/msa_proj/database"
            name       = "msa-ai-ml-db"
          }
        }
        restart_policy = "Always"
        volume {
          name = "msa-ai-ml-db"
          persistent_volume_claim {
            claim_name = "msa-ai-ml-db"
          }
        }
      }
    }
  }
}
