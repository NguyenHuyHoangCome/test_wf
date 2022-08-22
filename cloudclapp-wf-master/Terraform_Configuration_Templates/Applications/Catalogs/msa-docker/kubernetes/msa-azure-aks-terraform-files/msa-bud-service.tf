resource "kubernetes_service" "msa-bud" {

  metadata {
    name = "msa-bud"
    labels = {
      service = "msa-bud"
    }
  }
  spec {
    selector = {
      service = "msa-bud"
    }
    port {
      name        = "28170"
      port        = 28170
      target_port = 28170
    }
  }
}
