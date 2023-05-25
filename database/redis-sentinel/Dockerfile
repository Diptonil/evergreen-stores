FROM redis:6.0-alpine

ENV SENTINEL_QUORUM 2
ENV SENTINEL_DOWN_AFTER 5000
ENV SENTINEL_FAILOVER 60000

ADD sentinel.conf /etc/redis/sentinel.conf

RUN chown redis:redis /etc/redis/sentinel.conf

COPY sentinel-entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/sentinel-entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["sentinel-entrypoint.sh"]