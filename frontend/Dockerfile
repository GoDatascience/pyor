FROM node:8

MAINTAINER fernandocamargoti <fernando.camargo.ti@gmail.com>

ENV PYOR_FRONTEND=/usr/src/app

ADD package.json /tmp/package.json
WORKDIR /tmp

RUN npm install

VOLUME ["$PYOR_FRONTEND"]

WORKDIR $PYOR_FRONTEND

EXPOSE 4200

CMD ["npm", "start"]
