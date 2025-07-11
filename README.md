# CSVCruncher CLI

Простой CLI-скрипт для обработки CSV-файлов с поддержкой фильтрации, агрегации и сортировки.

## Возможности
- Фильтрация по условию (`<`, `>`, `=`)
- Агрегация (`avg`, `min`, `max`, `median`)
- Сортировка по колонке
- Ограничение количества отображаемых записей (head)

## Быстрый старт
1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Запустите скрипт:
   ```bash
   python csvcruncher.py --file products.csv [--where <условие>] [--aggregate <колонка=операция>] [--order-by <колонка=asc|desc>] [--head <количество записей>]
   ```

## Примеры
- Вывести первые 5 строк:
  ```bash
  python csvcruncher.py --file products.csv --head 5
  ```
- Фильтрация:
  ```bash
  python csvcruncher.py --file products.csv --where price>100
  ```
- Агрегация:
  ```bash
  python csvcruncher.py --file products.csv --aggregate price=avg
  ```
- Сортировка:
  ```bash
  python csvcruncher.py --file products.csv --order-by price=desc
  ```

## Тесты
Запуск тестов:
```bash
pytest --maxfail=1 --disable-warnings -v
```
