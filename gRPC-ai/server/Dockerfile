FROM node:20.24-alpine

WORKDIR /app

COPY server/package.json ./server/package.json

WORKDIR /app/server

RUN npm install

WORKDIR /app

COPY protos ./protos
COPY server ./server

WORKDIR /app/server

EXPOSE 50051

CMD ["npm", "start"]