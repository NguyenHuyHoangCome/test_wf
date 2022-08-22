--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4
-- Dumped by pg_dump version 12.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Data for Name: client; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.client (cli_id, cli_nom, cli_adr1, cli_adr2, cli_adr3, cli_codpos, cli_ville, cli_pays, cli_prefix, cli_lastupdate, cli_lastupdate_id, cli_ip_addr, cli_ip_mask, cli_istrusted, cli_factor, cli_type) FROM stdin;
2	MSAE2E							MSA	2020-05-20 11:44:49.399219	1			0	\N	
3	UBIE2E							UBI	2020-05-20 11:45:00.873362	1			0	\N	
\.


--
-- Data for Name: abonne; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.abonne (abo_cli, abo_id, abo_company, civilite, nom, prenom, abo_adr1, abo_adr2, abo_adr3, abo_codpos, abo_ville, abo_pays, abo_misc, abo_lastupdate_id, abo_lastupdate, abo_external_reference, abo_node_id, abo_type) FROM stdin;
3	6	0		UBI-E2E								1	0	2020-05-20 11:45:28.860198	UBI	\N	
2	7	0		MSA-E2E								1	0	2020-05-20 11:45:32.600572	MSA	\N	
\.


--
-- Data for Name: contact; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.contact (con_id, con_civil, con_nom, con_prenom, con_tel, con_email, con_fax, con_adr1, con_adr2, con_adr3, con_codpos, con_ville, con_pays, con_natact, con_dialang, con_ackmail, con_lastupdate, con_lastupdate_id) FROM stdin;
84	\N	\N	\N										\N	\N	0	2020-05-20 11:45:28.860198	1
85	\N	\N	\N										\N	\N	0	2020-05-20 11:45:32.600572	1
87		\N	\N										\N	\N	0	2020-05-20 11:46:28.847309	1
89		\N	\N										\N	\N	0	2020-05-20 11:46:55.655176	1
91		\N	\N										\N	\N	0	2020-09-10 11:13:39.210231	1
\.


--
-- Data for Name: abocon; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.abocon (abo_id, con_id, con_privileged) FROM stdin;
6	84	1
7	85	1
\.


--
-- Data for Name: aboges; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.aboges (ges_id, abo_id, pfl_id) FROM stdin;
\.


--
-- Data for Name: actor; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.actor (act_id, act_cli_id, act_login, act_password, act_type, act_external_id, act_role, act_otp, act_otp_valid, act_pfl_id, act_ext_authentication, pswd_update) FROM stdin;
38	3	UBIE2E6		A	6	5	\N	2020-05-20 11:45:28.860198	\N	0	\N
39	2	MSAE2E7		A	7	5	\N	2020-05-20 11:45:32.600572	\N	0	\N
40	2	LinuxLc125	324e0c4c6e0ed39f8fbab296d3b4b95d487ef21c	S	125	6	\N	2020-05-20 11:46:28.842934	\N	0	\N
42	3	AWSME127	d63a707a661a33c3a749c6fd9490a58c84e91357	S	127	6	\N	2020-09-10 11:13:39.202741	\N	0	\N
\.


--
-- Data for Name: clicon; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.clicon (con_id, cli_id) FROM stdin;
\.


--
-- Data for Name: ges_cli; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.ges_cli (cli_id, ges_id) FROM stdin;
2	1
3	1
\.


--
-- Data for Name: site; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.site (sit_id, sit_abo, sit_nom, sit_adr1, sit_adr2, sit_adr3, sit_codpos, sit_ville, sit_pays, sit_misc, sit_lastupdate_id, sit_lastupdate, sit_external_reference, sit_sealing_passwd, sit_valid_subscribe, sit_catalog_visibility, sit_price_class, sit_price_code, sit_tva_code, sit_billing_id, sit_billing_date, sit_gnudip_date, sit_date_create, sit_latitude, sit_longitude, sit_product_name, sit_geo_id) FROM stdin;
125	7	LinuxLocal								0	2020-05-20 11:46:28.835138	MSA125		1	1	A	1	0		2020-05-20 00:00:00	2020-05-20 11:46:28.835138	2020-05-20 11:46:28.835138	0	0		\N
127	6	AWSME								0	2020-09-10 11:13:39.194003	UBI127		1	1	A	1	0		2020-09-10 00:00:00	2020-09-10 11:13:39.194003	2020-09-10 11:13:39.194003	0	0		\N
\.


--
-- Data for Name: sitcon; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.sitcon (sit_id, con_id) FROM stdin;
125	87
127	91
\.


--
-- Data for Name: license; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.license (id, license_type, max_managed_entity, not_after, not_before, owner) FROM stdin;
18075096484084793194	DEV	\\xc30d04070302781d4c0f0e44e58e64d235013152fc8245d4526d3617935c855c8489915b37137db299d8cdb4ff5a8f758219384806f4ccbab3776afb284b673656f02eb5d80b	2022-04-16 00:00:00	2020-04-16 00:00:00	CN=dockerEduardo,O=UBiqube,OU=Ubiqube
\.


--
-- Data for Name: license_extensions; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.license_extensions (id, extensions, extensions_key, license_id) FROM stdin;
1	20012	1.3.6.1.4.1.13567.1.3.4	18075096484084793194
2	false	1.3.6.1.4.1.13567.1.3.3	18075096484084793194
3	DEV	1.3.6.1.4.1.13567.1.3.2	18075096484084793194
4	2500	1.3.6.1.4.1.13567.1.3.1	18075096484084793194
\.


--
-- Data for Name: msa_vars; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.msa_vars (var_name, var_value, var_lastupdated, comment) FROM stdin;
\.


--
-- Data for Name: sd; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.sd (sd_cli_prefix, sd_seqnum, sd_serial_number, sd_manufacturer, sd_model, sd_version, sd_login_entry, sd_passwd_entry, sd_type, sd_ip_config, sd_public_key, sd_external_connectivity, sd_internal_connectivity, sd_updated, sd_connected, sd_activated_vpn, sd_activated_fw, sd_activated_rv, sd_blacklisted, sd_client_shared_key, sd_usenat, sd_lastupdate, sd_lastupdate_id, sd_useclient, sd_firmware, sd_login_adm, sd_passwd_adm, sd_usentp_server, sd_ntpserver_addr, sd_alt_serial_number, man_id, mod_id, ver_id, sd_nat_traversal, sd_permanent_connection, sd_firstprovdate, sd_lastprovdate, sd_use_xauth, sd_xaclient_use_radius, sd_xaclient_login, sd_xaclient_passwd, sd_xaclient_ipconfig, sd_xacenter_ipradius, sd_xacenter_radius_port, sd_xacenter_pool_begin, sd_xacenter_pool_end, sd_xacenter_shared_passwd, sd_dns1, sd_dns2, sd_wins1, sd_wins2, sd_client_domain, sd_use_dhcp, sd_fw_current_rule, sd_fw_previous_rule, sd_nat_in_front, sd_nat_t_behind, sd_cli_ip_addr, sd_cli_ip_mask, sd_supported_client, sd_pfl_id, sd_hsrp1_ip_addr, sd_hsrp2_ip_addr, sd_hsrp_type, sd_hsrp_partner_id, sd_reboot_lastupdate, sd_reboot_flag, sd_hsrp_single, sd_backup_connectivity, sd_use_mod_config, sd_alert_mail, sd_log, sd_log_more, sd_ips_updated, sd_pfl_generic, sd_ips_pflid, sd_swapnet, sd_av_pflid, sd_asabaselicense, sd_asapluslicense, sd_log_report, sd_hostname, sd_snmp_community, sd_monitor_pflid, sd_ftp_passwd, sd_ftp_activated, sd_scan_pflid, sd_use_vpn_report, sd_botnet_pflid, sd_configuration_pflid, sd_management_port, sd_management_port_fallback, sd_monitoring_port, sd_staging_model, sd_activated_cert, sd_automatic_update, sd_starcenter_able, sd_family_id, sd_is_managed, sd_isutm, sd_isproxy, sd_conf_isipv6, sd_dpid, sd_node_name, sd_node_addr, sd_scan_ip_addr, sd_logarc_retention, sd_load_weight, sd_nature) FROM stdin;
MSA	125		Linux	Generic				H			E	N	0	0	0	0	0	0		0	2020-05-20 11:46:28.854817	1	0				0			14020601	14020601	0	0	0	\N	\N	0	0					1812			\N						0							0	0			0	0	\N	0	0	N	0	0	0	0	0	0	0	0	0			0			0		0	0	0	0	0	22	0	161		1	0	0	14020601	1	0	0	0		\N	\N		0	1	0
UBI	127		AWS	Generic				H			E	N	0	0	0	0	0	0		0	2020-09-10 11:13:39.219674	1	0				0			17010301	17010301	0	0	0	\N	\N	0	0					1812			\N						0							0	0			0	0	\N	0	0	N	0	0	0	0	0	0	0	0	0			0	\N		0		0	0	0	0	0	22	0	161		1	0	0	0	1	0	0	0		\N	\N		0	1	0
\.


--
-- Data for Name: sd_dhcp_server; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.sd_dhcp_server (sd_seqnum, int_connectivity_side, int_ordernum, sd_dhcp_domain, sd_dhcp_pool_begin, sd_dhcp_pool_end, sd_dhcp_dns1, sd_dhcp_dns2, sd_dhcp_wins1, sd_dhcp_wins2) FROM stdin;
125	I	0							
127	I	0							
\.


--
-- Data for Name: sd_features; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.sd_features (sd_seqnum, last_update, use_antivirus, use_webfilter, use_antispam, use_ips, use_dmz, use_ha, use_vpn, use_tamper_proof, use_qos, use_voip, use_botnet) FROM stdin;
125	2020-05-20 11:46:28.86816	0	0	0	0	0	0	0	0	0	0	0
127	2020-09-10 11:13:39.235049	0	0	0	0	0	0	0	0	0	0	0
\.


--
-- Data for Name: sd_interface; Type: TABLE DATA; Schema: redone; Owner: postgres
--

COPY redone.sd_interface (sd_cli_prefix, sd_seqnum, int_type, int_connectivity_side, int_name, int_ip_type, int_ip_addr, int_ip_mask, int_ip_gw, int_dns_1, int_dns_2, int_isp_login, int_isp_passwd, int_pabx_prefix, int_isp_phone, int_vpi, int_vci, int_eth_speed, int_eth_duplex, int_eth_type, int_rfc1483, int_physical_name, int_bandwidth, int_use_qos, int_security_level, int_vlan, int_ispublic, int_ips_activated, int_framerelay_ietf, int_sub_interface, int_dlci_number, int_framerelay_map_ip, int_framerelay_map_dlci, int_ordernum, int_isvoicelan, int_mac_addr, int_domain_name, int_ipv6_addr, int_use_ipv6, int_ipv6_mask, int_ipv6_gateway) FROM stdin;
MSA	125	E	E	ssh	S	127.0.0.1	255.255.255.255		\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	F	0	ssh	0	0	0	0	0	0	0	\N	\N	\N	\N	0	0	\N	\N		0	0	\N
UBI	127	E	E	eth0	S	10.0.1.28	255.255.255.255		\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	F	0	eth0	0	0	0	0	0	0	0	\N	\N	\N	\N	0	0	\N	\N		0	0	\N
\.


--
-- Data for Name: historique; Type: TABLE DATA; Schema: redsms; Owner: postgres
--

COPY redsms.historique (h_date, h_object, h_attribute, h_id, h_type, h_assettype, h_old_value, h_new_value, h_action) FROM stdin;
2020-05-20 11:46:28.93753	SD	sd_ip_config	125	VARCHAR2	1	void	127.0.0.1	INSERT
2020-05-20 11:46:55.731214	SD	sd_ip_config	126	VARCHAR2	1	void	127.0.0.1	INSERT
2020-09-10 11:12:46.405078	SD	sd_ip_config	126	VARCHAR2	1	127.0.0.1	void	DELETE
2020-09-10 11:13:39.318012	SD	sd_ip_config	127	VARCHAR2	1	void	10.0.1.28	INSERT
\.


--
-- Data for Name: sd; Type: TABLE DATA; Schema: redsms; Owner: postgres
--

COPY redsms.sd (sd_cli_prefix, sd_seqnum, sd_serial_number, sd_login_entry, sd_passwd_entry, sd_type, sd_ip_config, sd_public_key, sd_updated, sd_connected, sd_activated_vpn, sd_activated_fw, sd_client_shared_key, sd_usenat, sd_useclient, sd_login_adm, sd_passwd_adm, sd_cert_status, sd_cert_lastupdate, sd_cert_failure_message, sd_nat_traversal, sd_permanent_connection, sd_virtual_ip, sd_use_xauth, sd_use_dhcp, sd_locked, sd_soft_failure_message, sd_soft_lastupdate, sd_soft_status, sd_net_failure_message, sd_net_lastupdate, sd_net_status, sd_prov_lock, sd_fw_current_rule, sd_config_step, sd_cli_ip_addr, sd_cli_ip_mask, sd_supported_client, man_id, mod_id, ver_id, pfl_id, sd_hsrp1_ip_addr, sd_hsrp2_ip_addr, sd_hsrp_type, sd_hsrp_partner_id, sd_reboot_status, sd_reboot_lastupdate, sd_reboot_failure_message, sd_action, sd_hsrp_single, sd_use_mod_config, sd_alert_mail, sd_log, sd_log_more, sd_ips_updated, sd_ips_pflid, sd_ips_policy, sd_av_pflid, sd_av_notification, sd_av_type, sd_asabaselicense, sd_asapluslicense, sd_av_sigstatus, sd_url_pflid, sd_url_default_action, sd_url_category_filter, sd_as_pflid, sd_as_default_action, sd_as_type, sd_as_notification, sd_url_status, sd_as_status, sd_family_id, sd_log_report, sd_asset_update, sd_ips_activated_vpn, sd_hostname, sd_snmp_community, sd_monitor_pflid, sd_ftp_passwd, sd_poll_mode, sd_ftp_activated, sd_abo_id, sd_activated_net, sd_activated_voip, sd_admin_proto, sd_use_vpn_report, sd_external_reference, sd_botnet_pflid, sd_botnet_automatic_update, sd_configuration_pflid, sd_ha_isactive, sd_management_port, sd_management_port_fallback, sd_monitoring_port, sd_activated_cert, sd_automatic_update, sd_node_name, sd_node_addr, sd_man_name, sd_mod_name, sd_conf_isipv6, sd_dpid, sd_logarc_retention, sd_abo_external_ref) FROM stdin;
MSA	125	\N			H	127.0.0.1	\N	0	0	0	0	\N	1	0			N	2020-05-20 11:46:28.93753	\N	0	0	\N	0	0	\N	\N	2020-05-20 11:46:28.93753	N	\N	\N	N	-1	\N	0			\N	14020601	14020601	\N	0	\N	\N	0	0	N	\N	\N	0	0	0	0	0	0	0	0	0	\N	0	\N	\N	\N	0	\N	0	0	\N	0	\N	\N	\N	\N	0	0	0	0			0		\N	0	7	1	0	0	0	MSA125	0	0	0	0	22	0	161	1	0			Linux	Generic	0		\N	MSA
UBI	127	\N			H	10.0.1.28	\N	0	0	0	0	\N	1	0			N	2020-09-10 11:13:39.318012	\N	0	0	\N	0	0	\N	\N	2020-09-10 11:13:39.318012	N	\N	\N	N	-1	\N	0			\N	17010301	17010301	\N	0	\N	\N	0	0	N	\N	\N	0	0	0	0	0	0	0	0	0	\N	0	\N	\N	\N	0	\N	0	0	\N	0	\N	\N	\N	\N	0	0	0	0			0		\N	0	6	1	0	0	0	UBI127	0	0	0	0	22	0	161	1	0			AWS	Generic	0		\N	UBI
\.


--
-- Data for Name: sd_interface; Type: TABLE DATA; Schema: redsms; Owner: postgres
--

COPY redsms.sd_interface (sd_cli_prefix, sd_seqnum, int_type, int_connectivity_side, int_name, int_ip_type, int_ip_addr, int_ip_mask, int_ip_gw, int_dns_1, int_dns_2, int_isp_login, int_isp_passwd, int_pabx_prefix, int_isp_phone, int_vpi, int_vci, int_eth_speed, int_eth_duplex, int_eth_type, int_rfc1483, int_physical_name, int_bandwidth, int_use_qos, int_security_level, int_vlan, int_ispublic, int_ips_activated, int_framerelay_ietf, int_sub_interface, int_dlci_number, int_framerelay_map_ip, int_framerelay_map_dlci, int_frame_relay_ietf, int_ordernum, int_isvoicelan, int_mac_addr, int_domain_name, int_ipv6_addr, int_use_ipv6, int_ipv6_mask, int_ipv6_gateway) FROM stdin;
MSA	125	E	E	ssh	S	127.0.0.1	255.255.255.255				\N	\N	\N	\N	\N	\N	AUTO	AUTO	E	0	ssh	0	0	0	0	0	0	0		\N	\N	\N	0	0	0	\N			0	0	\N
UBI	127	E	E	eth0	S	10.0.1.28	255.255.255.255				\N	\N	\N	\N	\N	\N	AUTO	AUTO	E	0	eth0	0	0	0	0	0	0	0	 	\N	\N	\N	0	0	0	\N			0	0	\N
\.


--
-- Name: id_abonne; Type: SEQUENCE SET; Schema: redone; Owner: postgres
--

SELECT pg_catalog.setval('redone.id_abonne', 7, true);


--
-- Name: id_actor; Type: SEQUENCE SET; Schema: redone; Owner: postgres
--

SELECT pg_catalog.setval('redone.id_actor', 42, true);


--
-- Name: id_contact; Type: SEQUENCE SET; Schema: redone; Owner: postgres
--

SELECT pg_catalog.setval('redone.id_contact', 91, true);


--
-- Name: id_site; Type: SEQUENCE SET; Schema: redone; Owner: postgres
--

SELECT pg_catalog.setval('redone.id_site', 127, true);


--
-- Name: id_update; Type: SEQUENCE SET; Schema: redone; Owner: postgres
--

SELECT pg_catalog.setval('redone.id_update', 1109, true);


--
-- PostgreSQL database dump complete
--

