resource "kubernetes_deployment" "msa-kibana" {

  metadata {
    name = "msa-kibana"
    labels = {
      service = "msa-kibana"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "msa-kibana"
      }
    }
    strategy {
      type = "Recreate"
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "msa-kibana"
        }
      }
      spec {
        container {
          image = var.msa2_kibana_img
          name  = "msa-kibana"
          env {
            name  = "ELASTICSEARCH_HOSTS"
            value = "http://msa-es:9200"
          }
          env {
            name  = "ELASTICSEARCH_URL"
            value = "http://msa-es:9200"
          }
          env {
            name  = "ES_CREDENTIALS"
            value = "c3VwZXJ1c2VyOnheWnl1R002fnU9K2ZZMkc="
          }
          port {
            container_port = 5601
          }
        }
        restart_policy = "Always"
      }
    }
  }
}
