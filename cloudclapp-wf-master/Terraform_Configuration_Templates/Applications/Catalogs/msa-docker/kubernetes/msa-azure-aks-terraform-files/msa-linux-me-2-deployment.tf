resource "kubernetes_deployment" "linux-me-2" {

  metadata {
    name = "linux-me-2"
    labels = {
      service = "linux-me-2"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "linux-me-2"
      }
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "linux-me-2"
        }
      }
      spec {
        hostname = "linux-me-2"
        container {
          image = var.msa2_linuxme_img
          name  = "linux-me-2"
          port {
            container_port = 22
          }
          security_context {
            capabilities {
              add = ["NET_ADMIN", "NET_RAW", "DAC_READ_SEARCH", "sys_rawio"]
            }
            privileged = true
          }
        }
        restart_policy = "Always"
      }
    }
  }
}
