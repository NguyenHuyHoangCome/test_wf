resource "kubernetes_service" "msa-kibana" {

  metadata {
    name = "msa-kibana"
    labels = {
      service = "msa-kibana"
    }
  }
  spec {
    selector = {
      service = "msa-kibana"
    }
    port {
      name        = "5601"
      port        = 5601
      target_port = 5601
    }
  }
}
