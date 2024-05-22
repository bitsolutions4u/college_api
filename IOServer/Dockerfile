FROM node:16

# Create app directory
WORKDIR /app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

# RUN npm install
# If you are building your code for production
RUN npm ci --only=production

# Bundle app source
COPY . .

# Default Values of Dynamic Args 
ARG IO_PORT=8080 
ARG IO_SECRET='secrtyuasdfghewrtyudfghs'

# Updating the Env Variables
ENV IO_PORT=$IO_PORT
ENV IO_SECRET=$IO_SECRET

# RUN echo "$IO_PORT"

EXPOSE $IO_PORT

CMD [ "node", "server.js" ]
