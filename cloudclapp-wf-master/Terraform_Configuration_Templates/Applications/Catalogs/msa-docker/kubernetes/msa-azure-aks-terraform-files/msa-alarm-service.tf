resource "kubernetes_service" "msa-alarm" {

  metadata {
    name = "msa-alarm"
    labels = {
      service = "msa-alarm"
    }
  }
  spec {
    selector = {
      service = "msa-alarm"
    }
    port {
      name        = "28164"
      port        = 28164
      target_port = 28164
    }
  }
}
