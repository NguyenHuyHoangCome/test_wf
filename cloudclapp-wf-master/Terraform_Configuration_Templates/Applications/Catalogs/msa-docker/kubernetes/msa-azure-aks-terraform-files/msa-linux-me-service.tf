resource "kubernetes_service" "linux-me" {

  metadata {
    name = "linux-me"
    labels = {
      service = "linux-me"
    }
  }
  spec {
    selector = {
      service = "linux-me"
    }
    port {
      name        = "2224"
      port        = 2224
      target_port = 22
    }
  }
}
