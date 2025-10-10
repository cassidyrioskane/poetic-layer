# ---------- Stage 1: Build React app ----------
FROM node:18-alpine AS build
WORKDIR /app

# Copy dependency manifests
COPY frontend/package*.json ./
RUN npm install

# Copy source
COPY frontend/src ./src
COPY frontend/public ./public

# The build picks up REACT_APP_API_URL from Compose at build time
RUN npm run build

# ---------- Stage 2: Serve with nginx ----------
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
