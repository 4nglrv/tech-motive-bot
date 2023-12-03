class HandlerNames:
    ADD_CLIENT_PREFIX = 'client_add'
    GET_CLIENT_PREFIX = 'client_get'

    def CLIENT_UPDATE(self, uid: str or None = None):
        return f'{self.GET_CLIENT_PREFIX}_update_data_{uid or ""}'

    def CLIENT_REMOVE(self, uid: str or None = None):
        return f'{self.GET_CLIENT_PREFIX}_remove_data_{uid or ""}'

    def CLIENT_GET(self, uid: str or None = None):
        return f"{self.GET_CLIENT_PREFIX}_data_{uid or ''}"

    def CLIENT_PAGINATION_LEFT(self, page: int or None = None):
        return f"{self.GET_CLIENT_PREFIX}_pagination_left_{page or ''}"

    def CLIENT_PAGINATION_RIGHT(self, page: int or None = None):
        return f"{self.GET_CLIENT_PREFIX}_pagination_right_{page or ''}"

    def BACK_TO_ALL_CLIENTS(self, page: int or None = None):
        return f'{self.GET_CLIENT_PREFIX}_back_to_all_{page or ""}'

    ALL_CLIENTS = f'{GET_CLIENT_PREFIX}_all'

    CLIENT_ADD_STATE_TO_DB = f'{ADD_CLIENT_PREFIX}_add_data'
    CLIENT_EDIT_STATE = f'{ADD_CLIENT_PREFIX}client_state_edit_data'
    CLIENT_CANCEL_ADD_STATE_TO_DB = f'{ADD_CLIENT_PREFIX}_add_data_cancel'
