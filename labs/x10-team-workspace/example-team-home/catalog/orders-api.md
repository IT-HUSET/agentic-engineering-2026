---
owner: team-order
stack: Kotlin 2, Spring Boot, Postgres 16
remote: git@github.com:betala/orders-api.git
path: ~/work/orders-api
test: ./gradlew test
depends_on: [infra]
---

# orders-api

Owns order status and payment matching. Other services read status through `GET /orders/{id}` and never write it.

- `./gradlew test` starts Postgres through Testcontainers and requires Docker.
- Migrations live in `src/main/resources/db/migration`. Never edit a migration that has run.
