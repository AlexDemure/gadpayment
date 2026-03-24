Сервис `http://localhost:8000/docs`

RabbitMQ `http://localhost:15672/` guest\guest

```bash
docker compose -f .compose/docker-compose.yml run --rm server alembic upgrade head
```

## Как работает outbox

1. API сохраняет запись в `payments`
2. В той же транзакции создаётся запись в `outbox`
3. Dispatcher читает записи, у которых `published is null`
4. Dispatcher публикует сообщение в RabbitMQ
5. После публикации ставится `outbox.published`
6. Consumer принимает событие и ставит `outbox.accepted`
7. Consumer эмулирует обработку платежа
8. При успехе:
   - обновляет `payment.status`
   - ставит `payment.processed`
   - отправляет webhook
   - ставит `outbox.completed`
9. При ошибке:
   - увеличивает `outbox.errors`
   - ставит `outbox.failed`
   - если попыток меньше лимита, сбрасывает `published` для повторной публикации

## Записи в БД
- `id`: `8401ca3c-d3ce-49b9-a311-6eab2cd92d1b`
- `amount`: `100`
- `currency`: `RUB`
- `description`: `string`
- `status`: `succeeded`
- `idempotency_key`: `1`
- `webhook_url`: `https://example.com/`
- `processed`: `2026-03-24 18:15:53.069653 +00:00`
- `created`: `2026-03-24 18:11:51.950734 +00:00`
- `updated`: `2026-03-24 18:15:53.069662 +00:00`
- `context`: `{"additionalProp1": {}}`
---
- `id`: `9f353818-6047-4ef9-b6c5-8388e5d9945d`
- `topic`: `payment.new`
- `errors`: `1`
- `created`: `2026-03-24 18:11:51.952173 +00:00`
- `updated`: `2026-03-24 18:15:53.071693 +00:00`
- `published`: `2026-03-24 18:15:48.014003 +00:00`
- `accepted`: `2026-03-24 18:15:48.029291 +00:00`
- `failed`: `2026-03-24 18:15:16.705795 +00:00`
- `completed`: `2026-03-24 18:15:53.071691 +00:00`
- `payload`: `{"payment_id": "8401ca3c-d3ce-49b9-a311-6eab2cd92d1b"}`
