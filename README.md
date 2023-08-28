[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Practicum.Yandex](https://img.shields.io/badge/-Practicum.Yandex-464646?style=flat&logo=Practicum.Yandex&logoColor=56C0C0&color=008080)](https://practicum.yandex.ru/)
# Парсер документации Python

## Описание проекта
Парсер документации Python и Python Enhancement Proposal (PEP), 
расположенных по url адресам: 
* *https://docs.python.org/3/* 

* *https://peps.python.org/*

## Развертывание проекта

1. Клонировать проект с GitHub.
2. Развернуть и активировать виртуальное окружение.
3. Установить зависимости из файла `requirements.txt`.

## Описание парсеров

В проекте реализованы следующие парсеры:

`whats_new` - собирает url адреса статей про обновления в последних версиях 
Питона, названия статей и их автора.

`latest_versions` - собирает url адреса последних версий Питона, их номера 
и статус.

`download` - скачивает архив документации в формате пдф текущей версии Питона.

`pep` - собирает статусы всех PEP, подсчитывает количество PEP в каждом статусе 
и общее количество PEP.

## Запуск парсеров

Команду запуска парсеров необходимо вводить в окне терминала, находясь в 
директории `src`.

Команда запуска парсеров: `python main.py <парсер> <аргументы>`

Позиционные и опциональные аргументы парсеров указаны ниже:

```bash
usage: main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python и Python Enhancement Proposal (PEP)

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```
