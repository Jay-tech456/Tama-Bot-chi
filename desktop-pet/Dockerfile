# ============================================
# TamaBotchi Desktop Pet - Dockerfile
# ============================================
# NOTE: Electron apps are desktop GUI applications.
# This Dockerfile builds the React frontend for
# development/preview purposes. For the full Electron
# desktop experience, run locally with:
#   npm run electron:dev
# ============================================

# -- Stage 1: Build the React app ------------- 
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .
RUN npx tsc --noEmit || true && npx vite build

# -- Stage 2: Serve the built app ------------- 
FROM node:20-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/dist ./dist

EXPOSE 5173

# Run the preview server
# To build & run:
#   docker build -t tamabotchi-pet .
#   docker run -p 5173:5173 tamabotchi-pet
CMD ["serve", "-s", "dist", "-l", "5173"]
