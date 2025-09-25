# Use Node.js for building frontend
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy all frontend source code
COPY . .

# Build production-ready files
RUN npm run build

# Serve static files with nginx
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 3000 (React dev) or 80 (nginx prod)
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
