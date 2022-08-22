#!/bin/bash

mkdir -p /opt/fmc_repository/{CommandDefinition,Process,Datafiles}

pushd /opt/fmc_repository/CommandDefinition/
ln -sf ../OpenMSA_MS/AWS AWS
ln -sf ../OpenMSA_MS/.meta_AWS .meta_AWS
ln -sf ../OpenMSA_MS/LINUX LINUX
ln -sf ../OpenMSA_MS/.meta_LINUX .meta_LINUX
ln -sf ../OpenMSA_MS/CISCO CISCO
ln -sf ../OpenMSA_MS/.meta_CISCO .meta_CISCO
ln -sf ../OpenMSA_MS/FORTINET FORTINET
ln -sf ../OpenMSA_MS/.meta_FORTINET .meta_FORTINET
ln -sf ../OpenMSA_MS/PALOALTO PALOALTO
ln -sf ../OpenMSA_MS/.meta_PALOALTO .meta_PALOALTO
ln -sf ../OpenMSA_MS/OPENSTACK OPENSTACK
ln -sf ../OpenMSA_MS/.meta_OPENSTACK .meta_OPENSTACK

# ln -s ../OpenMSA_WF/MICROSERVICES/ OpenMSA
# popd

# pushd /opt/fmc_repository/Process
# ln -s ../OpenMSA_WF/WORKFLOWS/ OpenMSA
