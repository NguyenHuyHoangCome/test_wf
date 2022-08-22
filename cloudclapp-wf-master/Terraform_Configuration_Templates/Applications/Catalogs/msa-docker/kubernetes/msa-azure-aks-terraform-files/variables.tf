variable "msa2_camunda_img" {}
variable "msa2_linuxme_img" {}
variable "msa2_ai_ml_img" {}
variable "msa2_alarm_img" {}
variable "msa2_api_img" {}
variable "msa2_bud_img" {}
variable "msa2_cerebro_img" {}
variable "msa2_db_img" {}
variable "msa2_dev_img" {}
variable "msa2_es_img" {}
variable "msa2_front_img" {}
variable "msa2_kibana_img" {}
variable "msa2_monitoring_img" {}
variable "msa2_sms_img" {}
variable "msa2_ui_img" {}


variable "msa2_ai_ml_db_pvc" {}
variable "msa2_api_logs_pvc" {}
variable "msa2_api_pvc" {}
variable "msa2_bud_logs_pvc" {}
variable "msa2_bulkfiles_pvc" {}
variable "msa2_db_pvc" {}
variable "msa2_dev_pvc" {}
variable "msa2_entities_pvc" {}
variable "msa2_es_pvc" {}
variable "msa2_repository_pvc" {}
variable "msa2_rrd_repository_pvc" {}
variable "msa2_sms_logs_pvc" {}
variable "msa2_svn_pvc" {}

variable "cluster_terraform_remote_state" {
  description = "kubernetes cluster terraform state file path"
}
