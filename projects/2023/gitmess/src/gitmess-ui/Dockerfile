FROM node:20
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . ./
RUN npm run build
RUN rm -rf src/ tests/

WORKDIR /app/build
ENV PORT="3001"
EXPOSE 3001
CMD ["node", "index.js"]
