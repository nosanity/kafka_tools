**Установка**

    pip install git+https://github.com/nosanity/kafka_tools/
    
добавить `kafka_tools` в `INSTALLED_APPS`, запустить миграции
    
**Настройки**

-   `KAFKA_TOOLS_MESSAGES_HANDLER`
строка - путь к функции, принимающей на вход параметры
`topic` (str) и `message` (dict). Лучше, чтобы функция вызывала
какую-то celery таску для асинхронной обработки сообщения
- `KAFKA_TOOLS_BOOTSTRAP_SERVERS`
строка или массив строк вида `'host[:port]'`
- `KAFKA_TOOLS_LISTEN_TOPICS` 
массив строк
- `KAFKA_TOOLS_PRODUCER_TIMEOUT`
таймаут отправки сообщения
- `KAFKA_TOOLS_CONNECTION_RETRY_TIMEOUT`
таймаут в секундах между попытками подключения к кафке для чтения
сообщений, если она недоступна
