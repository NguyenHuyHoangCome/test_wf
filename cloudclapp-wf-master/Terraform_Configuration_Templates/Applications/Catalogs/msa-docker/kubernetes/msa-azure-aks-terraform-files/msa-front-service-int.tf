resource "kubernetes_service" "msa-front-int" {

  metadata {
    name = "msa-front-int"
    labels = {
      service = "msa-front-int"
    }
  }
  spec {
    selector = {
      service = "msa-front"
    }
    port {
      name        = "80"
      protocol    = "TCP"
      port        = 80
      target_port = 80
    }
    port {
      name        = "514"
      protocol    = "UDP"
      port        = 514
      target_port = 514
    }
    port {
      name        = "162"
      protocol    = "UDP"
      port        = 162
      target_port = 162
    }
    port {
      name        = "69"
      protocol    = "UDP"
      port        = 69
      target_port = 69
    }
    port {
      name        = "5200"
      protocol    = "UDP"
      port        = 5200
      target_port = 5200
    }
  }
}
