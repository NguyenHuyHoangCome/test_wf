resource "kubernetes_service" "msa-sms" {

  metadata {
    name = "msa-sms"
    labels = {
      service = "msa-sms"
    }
  }
  spec {
    selector = {
      service = "msa-sms"
    }
    port {
      name        = "28165"
      port        = 28165
      target_port = 28165
    }
    port {
      name        = "28169"
      port        = 28169
      target_port = 28169
    }
    port {
      name        = "3690"
      port        = 3690
      target_port = 3690
    }
    port {
      name        = "28172"
      port        = 28172
      target_port = 28172
    }
  }
}
