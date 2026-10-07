# Yandex Wiki Client

Python-клиент для [API Яндекс Вики](https://yandex.ru/support/wiki/ru/api-ref/about).

## Требования

Python 3.10 или новее.

## Установка

Установка пакета напрямую из GitHub:

```bash
python -m pip install "git+https://github.com/yandex/yandex-wiki-client.git"
```

Вместе с библиотекой устанавливаются зависимости `httpx` и `pydantic`.

## Пример

Для хранения токена рекомендуется использовать переменную окружения.

```python
import os

from yandex_wiki_client import WikiClient

with WikiClient(
    oauth_token=os.environ["WIKI_TOKEN"],
    org_id=os.environ["WIKI_ORG_ID"],
) as wiki:
    page = wiki.pages.get_by_slug("users/example/page")
    print(page.id, page.title)

    notes = wiki.pages.create(
        "users/example/notes",
        "Заметки",
        content="Первая запись",
    )
    print(notes.slug)
```

Для авторизации требуется ровно один токен (`oauth_token` или `iam_token`) и ровно один идентификатор организации (`org_id`, `cloud_org_id`).

Пример авторизации с IAM-токеном:

```python
with WikiClient(
    iam_token=os.environ["WIKI_IAM_TOKEN"],
    cloud_org_id=os.environ["WIKI_CLOUD_ORG_ID"],
) as wiki:
    print(wiki.users.get_me().username)
```

Как выбрать тип токена и идентификатор организации, описано в статье [Доступ к API](https://yandex.ru/support/wiki/ru/api-ref/access). Там же описано, как создать OAuth-приложение с необходимыми скоупами и где найти идентификатор организации.

По умолчанию тайм-аут составляет 30 секунд. При сетевых ошибках и кодах ответа 429, 502, 503 и 504 выполняется до трёх повторных попыток. Для настройки тайм-аута и числа повторных попыток используются аргументы `timeout` и `retries`.

## Разделы API

Каждому разделу API соответствует отдельный атрибут `WikiClient`:

| Атрибут | Назначение |
| --- | --- |
| `pages` | чтение, создание, редактирование, удаление и перенос страниц |
| `page_access` | права доступа к страницам |
| `attachments` | вложения |
| `comments` | комментарии |
| `grids` | динамические таблицы |
| `operations` | статус асинхронных операций, например клонирования и переноса |
| `recovery_tokens` | восстановление удалённой страницы |
| `search` | поиск |
| `spaces` | пространства |
| `users` | текущий пользователь |

Описание HTTP-методов, параметров и ответов: [справочник API](https://yandex.ru/support/wiki/ru/api-ref/about).

## Ошибки

При некорректном сочетании токенов или идентификаторов организации выбрасывается исключение `ConfigError`.

При получении ответа с кодом 4xx или 5xx выбрасывается исключение `ApiError` или один из его подклассов. Исключение содержит поля `status_code`, `error_code` и `message`. Для отдельных ошибок предусмотрены специализированные классы, в том числе `PageNotFoundError`, `ForbiddenError`, `ValidationApiError`, `UnauthorizedError` и `RateLimitedError`.

Если после повторных попыток запрос не удалось выполнить из-за сетевой ошибки, выбрасывается исключение `NetworkError`.

## Лицензия

Apache 2.0. Порядок внесения изменений в проект описан в [CONTRIBUTING](CONTRIBUTING).
