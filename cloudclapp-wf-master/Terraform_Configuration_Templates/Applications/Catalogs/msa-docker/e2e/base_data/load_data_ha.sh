#!/bin/bash

TMP_LOG='/tmp/db_load.log'
CMD_FILE='e2e/base_data/run_cmds_ha.sh'
OPEN_MS_DIR='/tmp/OpenMSA_MS'
OPEN_WF_DIR='/tmp/OpenMSA_WF'
#give some time for the DB to come up
sleep 5

if [ -f "/usr/bin/zenity" ]; then
    "${CMD_FILE}" "${TMP_LOG}" | tee /tmp/db_load.log | \
        zenity --progress --no-cancel --title "MSA data loader" \
        --pulsate 2> /dev/null
else
    bash "${CMD_FILE}" "${TMP_LOG}" "LOG"
fi

# Restart containers
echo '# Restart API....'
docker service update msa_msa_api

echo '# Restart SMS....'
docker service update msa_sms

echo '# Waiting API restart....'
sleep 20

if [ -z "$1" ]; then
    echo 'Cleaning /tmp'
    rm -rf "${OPEN_MS_DIR}"
    rm -rf "${OPEN_WF_DIR}"
fi
