FROM node:14-alpine3.12
RUN mrdir /bot
WORKDIR /bot
COPY package.json /bot
COPY yarn.lock /bot
RUN yarn ci
COPY tsconfig.json /bot
COPY tsconfig.release.json /bot
COPY config.ts /bot
COPY /src /bot/src
RUN mkdir files
RUN yarn build

