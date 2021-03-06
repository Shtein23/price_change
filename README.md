# Скрипт для изменения цен на продукцию на сайте

## О скрипте

Создан в рамках нестабильности цен для их быстрого изменения на сайте при необходимости.
На основном сайте компании отсутствует возможность быстрого изменения в большом количестве. 

Обычная схема изменения такова:

Авторизация в админ панеле -> Переход на страницу товара -> Переход в настройки страницы -> Изменение цены -> Сохранение

На основе этого создан данный скрипт, который выполняет все эти функции в автоматическом режиме.

## Зависимости

1. *[chromedriver](https://chromedriver.storage.googleapis.com/index.html?path=98.0.4758.102/)* - драйвер Chrome версии 98
2. *Selenium* - для эмуляции взаимодействия с сайтом
3. *Pandas* - для работы с таблицами Excel

Для удобства они размещены в *requirements.txt*.

## Как это работает

Все цены хранятся в таблице Excel с названием Price.xlsx в следующем виде:

| Name    | Price  | Links       |
|:-------:|:------:|:-----------:|
| Товар 1 | 20000  | https://... |
| Товар 2 | 130000 | https://... |
| ... | ... | ... |
| Товар n | 240000 | https://... |

Скрипт считывает таблицу и поочередно переходит по ссылкам в списке исполняя выше описанный алгоритм. Если товары 
выделены в категорию, то ячейка с ссылкой могут быть пусты - на это есть специальная проверка.

Для авторизации в админ панеле, а также других настроек скрипта используется файл ***settings.ini***

На данный момент там прописаны:
* admin_panel - ссылка на админскую панель
* email - почта для входа
* password - пароль
* coeff - коэффициент умножения

Пример:
```
[site_1]
admin_panel = https://example.ru/administrator
email = example@mail.ru
pass = 12345678
coeff = 2
```

Последний используется для умножения текущей цены и получения новой. В теории данный скрипт может 
использовать любое значение - например привязка к доллару на сайте ЦБ России.

Плюсом ко всему добавлена специальная проверка - если ссылка на товар есть, а цена не указана, то скрипт выставит
отображение вместо цены текст "Под заказ" (это входит в возможности сайта). Если же цена указана, а текст выставлен, 
то скрипт его выключит и поставит цену.


## Запланированные обновления

Скрипт подразумевает развитие и расширение, а также возможное внедрение в общую систему управления для быстрого и
удобного доступа:
1. Изменение только тех цен на сайте, которые поменялись в файле
2. Рефакторинг кода
3. Добавление изменения на других сайтах компании
