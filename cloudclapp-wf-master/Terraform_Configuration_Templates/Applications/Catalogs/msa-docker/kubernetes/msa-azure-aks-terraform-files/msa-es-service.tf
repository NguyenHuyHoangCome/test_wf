resource "kubernetes_service" "msa-es" {

  metadata {
    name = "msa-es"
    labels = {
      service = "msa-es"
    }
  }
  spec {
    selector = {
      service = "msa-es"
    }
    port {
      name        = "9200"
      port        = 9200
      target_port = 9200
    }
  }
}
