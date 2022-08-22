resource "kubernetes_service" "msa-cerebro" {

  metadata {
    name = "msa-cerebro"
    labels = {
      service = "msa-cerebro"
    }
  }
  spec {
    selector = {
      service = "msa-cerebro"
    }
    port {
      name        = "9000"
      port        = 9000
      target_port = 9000
    }
  }
}
