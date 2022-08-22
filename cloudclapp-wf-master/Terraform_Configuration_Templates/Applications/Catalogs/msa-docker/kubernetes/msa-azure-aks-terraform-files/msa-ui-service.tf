resource "kubernetes_service" "msa-ui" {

  metadata {
    name = "msa-ui"
    labels = {
      service = "msa-ui"
    }
  }
  spec {
    selector = {
      service = "msa-ui"
    }
    port {
      name        = "8080"
      port        = 8080
      target_port = 8080
    }
  }
}
