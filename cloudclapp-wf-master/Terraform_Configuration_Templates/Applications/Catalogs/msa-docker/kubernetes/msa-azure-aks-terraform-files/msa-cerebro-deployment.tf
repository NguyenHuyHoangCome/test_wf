resource "kubernetes_deployment" "msa-cerebro" {

  metadata {
    name = "msa-cerebro"
    labels = {
      service = "msa-cerebro"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "msa-cerebro"
      }
    }
    strategy {
      type = "Recreate"
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "msa-cerebro"
        }
      }
      spec {
        container {
          image = var.msa2_cerebro_img
          name  = "msa-cerebro"
          env {
            name  = "AUTH_TYPE"
            value = "basic"
          }
          env {
            name  = "BASIC_AUTH_PWD"
            value = "N@X{M4tfw'5%)+35"
          }
          env {
            name  = "BASIC_AUTH_USER"
            value = "cerebro"
          }
          port {
            container_port = 9000
          }
          command = ["/opt/cerebro/bin/cerebro", "-Dhosts.0.host=http://msa-es:9200"]
        }
        restart_policy = "Always"
      }
    }
  }
}
