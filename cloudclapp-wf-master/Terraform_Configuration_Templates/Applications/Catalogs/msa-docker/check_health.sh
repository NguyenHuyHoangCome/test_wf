#!/bin/bash

echo 'Wait until all containers are healthy'

ALL_HEALTHY=0

check_container() {
    echo "Checking $1's health..."
    while ! docker-compose -p dev-msa ps | grep $1 | grep -q "healthy"; do
        if docker-compose -p dev-msa ps | grep $1 | grep -q "unhealthy"; then
            echo "$1 container is not healthy"
            exit 1
        fi

        if docker-compose -p dev-msa ps | grep $1 | grep -q "starting"; then
            echo "$1 is still starting..."
            sleep 10
        fi
    done

    echo "$1 container is healthy"
}

check_container msa_db_1
check_container msa_api_1
check_container msa_ui_1
check_container msa_front_1
check_container msa_sms_1
check_container msa_bud_1
check_container msa_alarm_1
check_container msa_monitoring_1
check_container msa_es_1


echo 'All containers are in a healthy state'
exit 0
