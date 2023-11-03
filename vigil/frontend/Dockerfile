FROM node:18.18.1-slim AS base

RUN corepack enable

COPY . /app

WORKDIR /app

RUN pnpm i --force
