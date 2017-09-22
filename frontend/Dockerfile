FROM node:8

MAINTAINER fernandocamargoti <fernando.camargo.ti@gmail.com>

ENV MREQ_FRONTEND=/usr/src/app

ADD package.json /tmp/package.json
WORKDIR /tmp

RUN npm install

VOLUME ["$MREQ_FRONTEND"]

WORKDIR $MREQ_FRONTEND

EXPOSE 4200

CMD ["npm", "start"]
