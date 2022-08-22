#!/usr/bin/env bash

# PERSISTENT VOLUMES
PV=$(ls ./persistentvolume | grep msa | awk '{print $NF}')
for i in $PV; do
  microk8s kubectl apply -f ./persistentvolume/$i;
done

# PERSISTENT VOLUME CLAIMS
PVC=$(ls ./persistentvolumeclaim | grep msa | awk '{print $NF}')
for i in $PVC; do
  microk8s kubectl apply -f ./persistentvolumeclaim/$i;
done

# DEPLOYMENTS
DPL=$(ls ./deployment | grep msa | awk '{print $NF}')
for i in $DPL; do
  microk8s kubectl apply -f ./deployment/$i;
done

# SERVICES
SVC=$(ls ./service | grep msa | awk '{print $NF}')
for i in $SVC; do
  microk8s kubectl apply -f ./service/$i;
done

# PORT FORWARDING
# kubectl port-forward --address 0.0.0.0 service/msa-front 65033:443
