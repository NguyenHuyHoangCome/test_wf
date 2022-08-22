resource "kubernetes_service" "db" {

  metadata {
    name = "db"
    labels = {
      service = "db"
    }
  }
  spec {
    selector = {
      service = "db"
    }
    port {
      name        = "5432"
      port        = 5432
      target_port = 5432
    }
  }
}
