# Описание
Тестовое задание на позицию backend-разработчик.
Добавление изображения с компьютера пользователя или по ссылке, изменение его размеров.
Оригиналы изображения сохраняются, их можно посмотреть в административной панели (admin, 1234)
Есть возможность изменить только ширину, только высоту, или оба параметра, иначе появится уведомление об ошибке. Если оставить поля ширины и высоты по умолчанию, то пропорции изображения сохранятся.

# Установка
- Создайте виртуальное окружение командой: `virtuealenv name`
- Активируйте его командой: `source name/bin/activate`
- Создайте папку для проекта и скопируйте в нее репозиторий, командой:
`https://github.com/Marshak2k7/idaproject_test.git`
- Используйте команду:
 ```python
 pip install requirements.txt
 ```
# Запуск
Запускайте проект, с помощью команды:
```python
python manage.py runserver
```
