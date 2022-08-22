<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */ 
function list_args()
{
  create_var_def('upd_rules.0.index', 'Integer');
  create_var_def('upd_rules.0.action', 'String');
}

foreach ( $context['upd_rules'] as $rule)
{
    foreach ($context['permit'] as $index => $policy) {
	if ($context['permit'][$index]['index'] == $rule['index']) {
            $context['permit'][$index]['action'] = $rule['action'];
        }
    }
}

unset($context['upd_rules']);

/**
 * End of the task do not modify after this point
 */
$ret = prepare_json_response(ENDED, 'Task OK', $context, true);
echo "$ret\n";

?>