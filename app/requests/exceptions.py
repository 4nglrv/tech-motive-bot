class ApiType:
    get_users = 'GET_ALL_USERS'
    get_user_by_id = 'GET_USER_BY_ID'
    update_user = 'UPDATE_USER'
    remove_user = 'REMOVE_USER'
    add_user = 'ADD_USER'


class ResponseNotFound(Exception):
    def __init__(self, message, chat_id=None, operation_type=None):
        super().__init__(message)

        self.message = message
        self.type = operation_type
        self.chat_id = chat_id


class ResponseBadRequest(Exception):
    def __init__(self, message, chat_id=None, operation_type=None):
        super().__init__(message)

        self.message = message
        self.type = operation_type
        self.chat_id = chat_id


class ResponseInternalServerError(Exception):
    def __init__(self, message, chat_id=None, operation_type=None):
        super().__init__(message)

        self.message = message
        self.type = operation_type
        self.chat_id = chat_id


