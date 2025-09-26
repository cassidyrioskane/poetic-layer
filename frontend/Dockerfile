# Stage 1: Build React app
FROM node:18-bullseye-slim AS build
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (react-scripts included)
RUN npm ci

# Copy frontend source code
COPY . ./

# Build production-ready app
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
