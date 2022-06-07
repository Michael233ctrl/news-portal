FROM node:18-alpine3.14

WORKDIR /client

ENV PATH /client/node_modules/.bin:$PATH

COPY package.json .
COPY package-lock.json ./

RUN npm install --silent

COPY . .

EXPOSE 3000

CMD ["npm", "start"]