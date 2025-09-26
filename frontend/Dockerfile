# Stage 1: Build React app
FROM node:18-alpine AS build

WORKDIR /app

# Copy package.json and package-lock.json
COPY frontend/package*.json ./

# Install dependencies (react-scripts included)
RUN npm install

# Copy only source files (avoid overwriting node_modules)
COPY frontend/src ./src
COPY frontend/public ./public

# Build production-ready files
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
