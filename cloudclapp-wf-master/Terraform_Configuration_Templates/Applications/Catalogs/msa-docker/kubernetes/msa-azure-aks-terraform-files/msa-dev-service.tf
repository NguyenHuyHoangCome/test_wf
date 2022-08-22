resource "kubernetes_service" "msa-dev" {

  metadata {
    name = "msa-dev"
    labels = {
      service = "msa-dev"
    }
  }
  spec {
    selector = {
      service = "msa-dev"
    }
    port {
      name        = "22"
      port        = 22
      target_port = 22
    }
  }
}
