#!/usr/bin/env bash

# DEPLOYMENTS
DPL=$(ls ./deployment | grep msa | awk '{print $NF}')
for i in $DPL; do
  microk8s kubectl delete -f ./deployment/$i;
done

# PERSISTENT VOLUME CLAIMS
PVC=$(ls ./persistentvolumeclaim | grep msa | awk '{print $NF}')
for i in $PVC; do
  microk8s kubectl delete -f ./persistentvolumeclaim/$i;
done

# PERSISTENT VOLUMES
PV=$(ls ./persistentvolume | grep msa | awk '{print $NF}')
for i in $PV; do
  microk8s kubectl delete -f ./persistentvolume/$i;
done

# SERVICES
SVC=$(ls ./service | grep msa | awk '{print $NF}')
for i in $SVC; do
  microk8s kubectl delete -f ./service/$i;
done
