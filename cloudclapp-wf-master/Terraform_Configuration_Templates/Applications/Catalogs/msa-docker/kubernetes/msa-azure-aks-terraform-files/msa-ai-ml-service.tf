resource "kubernetes_service" "msa-ai-ml" {

  metadata {
    name = "msa-ai-ml"
    labels = {
      service = "msa-ai-ml"
    }
  }
  spec {
    selector = {
      service = "msa-ai-ml"
    }
    port {
      name        = "8000"
      port        = 8000
      target_port = 8000
    }
  }
}
