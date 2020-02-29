FROM node as dev
WORKDIR /app

COPY package.json package-lock.json /app/
RUN npm install

EXPOSE 3000
CMD ["npm", "start"]


FROM node as prod-builder
WORKDIR /app

COPY package.json package-lock.json /app/
RUN npm install

COPY . /app
RUN npm run build


FROM nginx as prod

COPY --from=prod-builder /app/build/ /usr/share/nginx/html/
