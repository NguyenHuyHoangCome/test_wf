#!/bin/bash
set -e

TMP_LOG='/tmp/db_load.log'
CMD_FILE='e2e/base_data/run_cmds.sh'
OPEN_MS_DIR='/tmp/OpenMSA_MS'
OPEN_WF_DIR='/tmp/OpenMSA_WF'
#give some time for the DB to come up
echo "Wait 30s for the database to load all tables"
sleep 30

if [ -f "/usr/bin/zenity" ]; then
    "${CMD_FILE}" "${TMP_LOG}" | tee /tmp/db_load.log | \
        zenity --progress --no-cancel --title "MSA data loader" \
        --pulsate 2> /dev/null
else
    bash "${CMD_FILE}" "${TMP_LOG}" "LOG"
fi

# Restart containers
echo '# Restart API....'
docker restart "$(docker ps -q -f name=msa_api)"

echo '# Restart SMS....'
docker restart "$(docker ps -q -f name=msa_sms)"

echo '# Waiting API restart....'
sleep 20

if [ -z "$1" ]; then
    echo 'Cleaning /tmp'
    rm -rf "${OPEN_MS_DIR}"
    rm -rf "${OPEN_WF_DIR}"
fi
