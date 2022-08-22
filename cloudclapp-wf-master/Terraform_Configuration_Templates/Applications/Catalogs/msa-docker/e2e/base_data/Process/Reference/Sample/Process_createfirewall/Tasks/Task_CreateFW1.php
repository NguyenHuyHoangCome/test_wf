<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */ 
function list_args(){
  create_var_def('fw_name', 'String');
  create_var_def('sleep', 'Integer');
  create_var_def('device.0.id', 'Device');
}

sleep($context['sleep']);
/**
 * End of the task do not modify after this point
 */
$ret = prepare_json_response(ENDED, 'Task OK', $context, true);
echo "$ret\n";

?>
