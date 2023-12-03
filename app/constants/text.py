from app.requests.models import ClientDto


class TextBtn:
    CLIENTS = "Клиенты 👤"
    ORDERS = "Заказы (в разработке)"

    CHOOSE_SECTION = "Выберите раздел"

    ADD_CLIENT = "Добавить клиента"
    ALL_CLIENTS = "Все клиенты"
    IMPORT_CLIENTS = "Импортировать базу клиентов (в разработке)"
    CANCEL_ADD_CLIENT = "Отменить добавление клиента"
    MAIN_MENU = "Главное меню"

    ADD = "Добавить"
    EDIT = "Изменить"
    AGAIN = "Заново"
    REMOVE = "Удалить"
    REPEAT = "Повторить"
    CANCEL = "Отменить"
    BACK = "Вернуться назад"

    TRUE = "Есть"
    NONE = "Нет"

    PATRONYMIC_IS_NONE = "Нет отчества"
    ABOUT_IS_NONE = "Без дополнительной информации"


class TextMsg:
    RESPONSE_NOT_FOUND = "Не найдено. Попробуйте ввести другие данные"
    RESPONSE_BAD_REQUEST = "Некорректный запрос. Пожалуйста, повторите позже"
    RESPONSE_INTERNAL_SERVER_ERROR = "Ошибка сервера, повторите попытку чуть позже, скоро починим!"
    RESPONSE_UNKNOWN_EXCEPTION = "Неизвестная ошибка, скоро починим!"

    GET_CLIENTS_VALIDATION_ERR = "Возникла ошибка валидации входных данных с клиентами. " \
                                "Повторите попытку чуть позже, скоро починим!"
    GET_CLIENT_VALIDATION_ERR = "Возникла ошибка валидации входных данных с клиентом. " \
                                 "Повторите попытку чуть позже, скоро починим!"

    CANCELED = "Отменено"

    TYPE_FIRST_NAME = "Введите имя клиента"
    TYPE_LAST_NAME = "Введите фамилию клиента"
    TYPE_PATRONYMIC = "Введите отчество клиента"
    TYPE_CITY = 'Введите город клиента'
    TYPE_ADDRESS = 'Введите адрес клиента'
    TYPE_PHONE = 'Введите номер телефона клиента'
    INCORRECT_PHONE = 'Введен некорректный номер телефона, повторите попытку'
    TYPE_ABOUT_CLIENT = 'Введите дополнительную информацию о клиенте'

    CANCEL_ADD_CLIENT = "Отменить добавление клиента"
    SELECT_CLIENT_ACTION = 'Выберите действие над клиентами'
    CLIENTS_IN_DATABASE = 'База данных состоит из следующих клиентов:'
    ADD_FIRST_CLIENT = "Для начала добавьте хотя бы одного клиента =)"

    @staticmethod
    def CLIENT_ADD_CONFIRM(data: ClientDto):
        return f"Вы точно хотите создать клиента со следующей информацией?\n" \
               f"\n*Имя*: {data['first_name']}" \
               f"\n*Фамилия*: {data['last_name']}" \
               f"\n*Отчество*: {data['patronymic']}" \
               f"\n*Город*: {data['city']}" \
               f"\n*Адрес*: {data['address']}" \
               f"\n*Номер телефона*: {data['phone']}" \
               f"\n*Дополнительная информация*: {data['about_client']}"

    @staticmethod
    def CLIENT_ADD_ERROR(error):
        return f'Произошла непредвиденная ошибка при добавлении пользователя ({error})\n' \
               f'\nПовторить попытку?'

    @staticmethod
    def UNKNOWN_ERROR(error):
        return f"Неизвестная ошибка, повторите попытку ({error})"

    @staticmethod
    def CLIENT_FOUND(data: ClientDto):
        return f"По номеру телефона {data['phone']} найден следующий клиент:\n" \
               f"\n*ФИО*: {data['last_name']} {data['first_name']} {data['patronymic'] or ''}" \
               f"\n*Город*: {data['addresses'][0]['city']}" \
               f"\n*Адрес*: {data['addresses'][0]['address']}" \
               f"\n*Доп. информация*: {data['about_client'] or 'нет'}"

    @staticmethod
    def CLIENT_INFO(data: ClientDto):
        return f"\n*ФИО*: {data['last_name']} {data['first_name']} {data['patronymic'] or ''}" \
               f"\n*Номер телефона*: {data['phone']}" \
               f"\n*Город*: {data['addresses'][0]['city']}" \
               f"\n*Адрес*: {data['addresses'][0]['address']}" \
               f"\n*Доп. информация*: {data['about_client'] or 'нет'}"

    @staticmethod
    def CLIENT_NOT_FOUND(phone: str):
        return f"По номеру телефона {phone} не найдено ни одного клиента"
