<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */ 
function list_args(){
  create_var_def('permit.0.protocol', 'String');
  create_var_def('permit.0.action', 'String');
  create_var_def('permit.0.source_ip', 'IpAddress');
  create_var_def('permit.0.source_mask', 'IpMask');
  create_var_def('permit.0.wan_ip', 'IpAddress');
  create_var_def('permit.0.incoming_port', 'Integer');
  create_var_def('permit.0.lan_ip', 'IpAddress');
  create_var_def('permit.0.redirect_port', 'Integer');
}

sleep(10);

/**
 * End of the task do not modify after this point
 */
$ret = prepare_json_response(ENDED, 'Task OK', $context, true);
echo "$ret\n";

?>
