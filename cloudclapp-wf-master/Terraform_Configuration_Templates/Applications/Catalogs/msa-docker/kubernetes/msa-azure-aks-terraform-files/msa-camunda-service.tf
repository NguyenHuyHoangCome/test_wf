resource "kubernetes_service" "camunda" {

  metadata {
    name = "camunda"
    labels = {
      service = "camunda"
    }
  }
  spec {
    selector = {
      service = "camunda"
    }
    port {
      name        = "8080"
      port        = 8080
      target_port = 8080
    }
  }
}
