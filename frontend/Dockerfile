FROM node:8-onbuild

MAINTAINER fernandocamargoti <fernando.camargo.ti@gmail.com>

ENV PYOR_FRONTEND=/usr/src/app
ENV PATH=$NODE_MODULES/.bin:$PATH

WORKDIR $PYOR_FRONTEND

EXPOSE 4200

CMD ["npm", "start"]
