FROM node:lts-alpine as build-stage
EXPOSE 8080
RUN apk update && apk add vim bash && yarn global add @vue/cli
WORKDIR /app
COPY ./client/ ./
#CMD ["yarn", "serve"]
RUN yarn build
#
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist/ /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
