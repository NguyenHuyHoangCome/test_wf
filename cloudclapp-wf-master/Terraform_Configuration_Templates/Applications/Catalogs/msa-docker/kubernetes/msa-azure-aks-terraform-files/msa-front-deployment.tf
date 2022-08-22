resource "kubernetes_deployment" "msa-front" {

  metadata {
    name = "msa-front"
    labels = {
      service = "msa-front"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "msa-front"
      }
    }
    strategy {
      type = "Recreate"
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "msa-front"
        }
      }
      spec {
        container {
          image = var.msa2_front_img
          name  = "msa-front"
          port {
            container_port = 80
          }
          port {
            container_port = 443
          }
          port {
            container_port = 514
            protocol       = "UDP"
          }
          port {
            container_port = 162
            protocol       = "UDP"
          }
          port {
            container_port = 69
            protocol       = "UDP"
          }
          port {
            container_port = 5200
            protocol       = "UDP"
          }
          liveness_probe {
            exec {
              command = ["curl -k --fail https://localhost"]
            }
          }
        }
        restart_policy = "Always"
      }
    }
  }
}
