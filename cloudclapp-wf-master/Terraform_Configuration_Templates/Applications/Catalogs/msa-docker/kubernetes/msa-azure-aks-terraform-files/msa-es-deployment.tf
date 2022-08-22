resource "kubernetes_deployment" "msa-es" {

  metadata {
    name = "msa-es"
    labels = {
      service = "msa-es"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        service = "msa-es"
      }
    }
    strategy {
      type = "Recreate"
    }
    template {
      metadata {
        labels = {
          network_quickstart-default = "true"
          service                    = "msa-es"
        }
      }
      spec {
        container {
          image = var.msa2_es_img
          name  = "msa-es"
          env {
            name  = "ES_CREDENTIALS"
            value = "c3VwZXJ1c2VyOnheWnl1R002fnU9K2ZZMkc="
          }
          env {
            name  = "ES_JAVA_OPTS"
            value = "-Xms512m -Xmx1024m"
          }
          env {
            name  = "bootstrap.memory_lock"
            value = "true"
          }
          env {
            name  = "discovery.type"
            value = "single-node"
          }
          env {
            name  = "script.painless.regex.enabled"
            value = "true"
          }
          env {
            name  = "xpack.security.enabled"
            value = "true"
          }
          port {
            container_port = 9200
          }
          liveness_probe {
            exec {
              command = ["'test -f /home/install/init-done && curl -s -XGET -H ''Authorization: Basic c3VwZXJ1c2VyOnheWnl1R002fnU9K2ZZMkc=''  ''http://localhost:9200/_cluster/health?pretty'' | grep -q ''status.*green'' || exit 1'"]
            }
            failure_threshold     = 10
            initial_delay_seconds = 30
            period_seconds        = 10
            timeout_seconds       = 2
          }
          volume_mount {
            mount_path = "/usr/share/elasticsearch/data"
            name       = "msa-es"
          }
        }
        restart_policy = "Always"
        volume {
          name = "msa-es"
          persistent_volume_claim {
            claim_name = "msa-es"
          }
        }
      }
    }
  }
}
