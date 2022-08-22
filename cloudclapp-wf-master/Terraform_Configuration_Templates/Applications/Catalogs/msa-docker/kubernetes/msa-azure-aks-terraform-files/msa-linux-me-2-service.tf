resource "kubernetes_service" "linux-me-2" {

  metadata {
    name = "linux-me-2"
    labels = {
      service = "linux-me-2"
    }
  }
  spec {
    selector = {
      service = "linux-me-2"
    }
    port {
      name        = "2225"
      port        = 2225
      target_port = 22
    }
  }
}
