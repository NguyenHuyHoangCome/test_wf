resource "kubernetes_deployment" "linux-me" {

  metadata {
    name = "linux-me"
    labels = {
      service = "linux-me"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "linux-me"
      }
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "linux-me"
        }
      }
      spec {
        hostname = "linux-me"
        container {
          image = var.msa2_linuxme_img
          name  = "linux-me"
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
