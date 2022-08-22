resource "kubernetes_service" "msa-api" {

  metadata {
    name = "msa-api"
    labels = {
      service = "msa-api"
    }
  }
  spec {
    selector = {
      service = "msa-api"
    }
    port {
      name        = "8480"
      port        = 8480
      target_port = 8480
    }
    port {
      name        = "8787"
      port        = 8787
      target_port = 8787
    }
  }
}
