FROM node:18

WORKDIR /app

COPY reactjs/package.json reactjs/package-lock.json ./

RUN npm install

COPY reactjs/ .

RUN npm run build

EXPOSE 5173

CMD ["npm", "run", "dev"]
