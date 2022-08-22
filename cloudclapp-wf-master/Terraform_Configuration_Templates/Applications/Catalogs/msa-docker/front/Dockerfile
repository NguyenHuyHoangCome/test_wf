FROM nginx:1.21-alpine
RUN apk add nginx-mod-stream openssl && \
    apk upgrade
RUN mkdir -p /app/msa_version/
COPY version.html /app/msa_version/index.html
COPY swagger /app/swagger
COPY msa_sdk_doc /app/msa_sdk

RUN mkdir -p /etc/nginx/ssl

RUN openssl req -x509 -nodes \
    -days 365 \
    -subj "/C=CA/ST=QC/O=UBiqube/CN=msa2.ubiqube.com" \
    -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/server.key \
    -out    /etc/nginx/ssl/server.crt

RUN sed -i -e 's,include /etc/nginx/conf\.d/\*\.conf;,include /etc/nginx/conf.d/http_*.conf;,g' /etc/nginx/nginx.conf
RUN echo -e "\nstream {\n    include /etc/nginx/conf.d/stream_*.conf;\n}" >> /etc/nginx/nginx.conf
COPY http_nginx.conf /etc/nginx/conf.d/
COPY stream_syslogs.conf /etc/nginx/conf.d/
COPY stream_snmptraps.conf /etc/nginx/conf.d/
COPY stream_tftp.conf /etc/nginx/conf.d/
