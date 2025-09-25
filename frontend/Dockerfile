# Stage 1: Build React app
FROM node:18-alpine AS build
WORKDIR /app

# Copy package files first
COPY package.json package-lock.json ./

# Install all dependencies including devDependencies
RUN npm install

# Copy the rest of the source code
COPY . .

# Build the production app
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
