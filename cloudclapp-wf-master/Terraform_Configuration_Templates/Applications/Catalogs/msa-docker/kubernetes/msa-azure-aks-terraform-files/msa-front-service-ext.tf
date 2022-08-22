resource "kubernetes_service" "msa-front-ext" {

  metadata {
    name = "msa-front-ext"
    labels = {
      service = "msa-front-ext"
    }
  }
  spec {
    selector = {
      service = "msa-front"
    }
    type = "LoadBalancer"
    port {
      name        = "443"
      protocol    = "TCP"
      port        = 443
      target_port = 443
    }
  }
}
