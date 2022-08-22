resource "kubernetes_network_policy" "quickstart-default" {
  metadata {
    name = "quickstart-default"
  }
  spec {
    pod_selector {
      match_labels = {
        network_quickstart-default = "true"
      }
    }
    ingress {
      from {
        pod_selector {
          match_labels = {
            network_quickstart-default = "true"
          }
        }
      }
    }
    policy_types = ["Ingress"]
  }
}
