FROM node:20.11.1

RUN mkdir -p /app
WORKDIR /app

RUN npm install -g @angular/cli

COPY . /app
RUN npm i --legacy-peer-deps

EXPOSE 4200
CMD ["npm", "run", "start", "--", "--proxy-config", "proxy.config.json", "--host", "0.0.0.0", "--poll=1000", "--disable-host-check"]
