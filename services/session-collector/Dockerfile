FROM golang:1.25-alpine AS build
WORKDIR /src
COPY . .
RUN go build -o /session-collector ./

FROM alpine:3.18
COPY --from=build /session-collector /usr/local/bin/session-collector
EXPOSE 8001
CMD ["/usr/local/bin/session-collector"]
