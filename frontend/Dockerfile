# Stage 1: Build React app
FROM node:18-alpine AS build

WORKDIR /app

# Install deps
COPY frontend/package*.json ./
RUN npm install

# Copy source
COPY frontend/ ./

# Build production-ready files
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy build output to nginx html dir
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
