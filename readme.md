# SpellChecker and SpellCorrector
Версия 1.0

Автор: Цуп Илья (ilyatzup@gmail.com)

## Описание
Данное приложение является консольной версией SpellCorrector'а, который 
поддерживает большинство языков мира.
В качестве словарей для проверки, присутствуют готовые словари русского
и английского языков, а также возможность создать собственный словарь
для любого языка через утилиту dictionary_creator.


## Требования
* Python версии не ниже 3.6


## Состав
* Консольная версия SpellCorrector: `spellcorrector.py`
* Консольная версия Dictionary Creator: `dictionary_creator.py`
* Консольная версия Dictionary Downloader: `dictionary_downloader.py`
* Модули: `SpellCorrector/`
* Тесты: `Tests/`
* Готовые словари: `Correct Dictionaries`


## Консольная версия SpellCorrector
Имеет 2 режима работы:
* 1) Mispellings
Выводит на экран ошибки в формате `line:index` {'word': 'WORD'`, 'correction': ['CORR1', 'CORR2']`}
* 1.1) [-c], [--coordinate] - эти флаги добавляют к выводу координаты в виде line:index.
* 1.2) [-correct] amount - этот флаг позволяет исправить amount ошибок и выводит их в соответствующем формате.
* 2) Mistake Finder
Выводит на экран ошибки в указанном выше формате без координат и исправлений.
Пример запуска: `./spellcorrector.py --infile Texts\HarryPotterText.txt mistake_finder 10`
Более подробная справка по запуску: `./spellcorrector.py --help`


## Консольная версия Dictionary Creator
Утилита, позволяющая работать со словарями.
Имеет 4 режима работы:
* 1) Add
Добавляет слово к выбранному словарю.
* 2) Append
Добавляет второй словарь к первому.
* 3) Merge
Складывает два словаря и кладёт их в отдельный словарь.
* 4) Create
Создаёт словарь из данного текста.
Пример запуска: `./dictionary_creator.py add Zeliboba "Correct Dictionaries/large.dic"`
Более подробная справка по запуску: `./dictionary_creator.py --help`

## Консольная версия Dictionary Downloader
Скачивает два словаря: русский и английский. Кладёт их в папку Correct Dictionaries.
Пример запуска: `./dictionary_downloader.py`


## Подробности реализации
Программа поддерживает переносы строк, пропущенные пробелы, опечатки в словах.
Модуль, реализующий логику подсчёта расстояния Левенштейна -
`SpellCorrector/levenshtein_distance_counter.py`. Он основан на работе с бором(trie)
и подсчёт расстояния осуществляется засчёт перебора дерева с эвристической оптимизацией.
Пропущенные пробелы отрабатываются перебором вариантов в `spellcorrector.py`. 

