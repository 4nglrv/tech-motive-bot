import json

import requests

from app.actions.clients.keyboards import add_client_reply_keyboard
from app.common.enviroments import API_URL
from app.constants.text import TextMsg
from app.requests.exceptions import ResponseNotFound, ResponseBadRequest, ResponseInternalServerError
from app.requests.models import GetClientsReqDto, ClientDto, ClientSuccessResDto
from telebot.async_telebot import AsyncTeleBot


class API:
    def __init__(self, bot: AsyncTeleBot, chat_id: int, url=f'http://{API_URL}'):
        self.url = url
        self.limit = 10
        self.bot = bot
        self.chat_id = chat_id

    async def __get_response_data(self, response):
        data = response.json()

        try:
            if response.status_code == 400:
                raise ResponseBadRequest(data)
            if response.status_code == 404:
                raise ResponseNotFound(data)
            if response.status_code == 500:
                raise ResponseInternalServerError(f'Ошибка сервера: {data}')
            if response.status_code == 200 or 201:
                return response.json()
            else:
                raise Exception(f'Неизвестная ошибка: {data}')

        except ResponseNotFound as e:
            await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=f'{TextMsg.RESPONSE_NOT_FOUND}\n```Error_log: {e.message}```',
                    parse_mode='Markdown'
                )

        except ResponseBadRequest as e:
            await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=f'{TextMsg.RESPONSE_BAD_REQUEST}\n```Error_log: {e.message}```',
                    parse_mode='Markdown'
                )

        except ResponseInternalServerError as e:
            await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=f'{TextMsg.RESPONSE_INTERNAL_SERVER_ERROR}\n```Error_log: {e.message}```',
                    parse_mode='Markdown'
                )

        except Exception as e:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f'{TextMsg.RESPONSE_UNKNOWN_EXCEPTION}\n```Error_log: {e}```',
                parse_mode='Markdown'
            )

    async def get_clients(self, page=1) -> GetClientsReqDto:
        response = requests.get(
            f"{self.url}/clients/get?limit={self.limit}&page={page}",
        )

        data = await self.__get_response_data(response)

        try:
            GetClientsReqDto(**data)
            return data

        except ValueError as e:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f'{TextMsg.GET_CLIENTS_VALIDATION_ERR}\n```Error_log: {e.errors()}```',
                parse_mode='Markdown'
            )

    async def get_client_by_phone(self, phone: str) -> ClientDto:
        response = requests.get(
            f"{self.url}/clients/getByPhone/{phone}",
        )

        try:
            data = await self.__get_response_data(response)
            ClientDto(**data)
            return data

        except ValueError as e:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f'{TextMsg.GET_CLIENT_VALIDATION_ERR}\n```Error_log: {e.errors()}```',
                parse_mode='Markdown'
            )

    async def get_client_by_id(self, uid: str):
        response = requests.get(
            f"{self.url}/clients/getById/{uid}"
        )

        data = await self.__get_response_data(response)

        try:
            ClientDto(**data)
            return data

        except ValueError as e:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f'{TextMsg.GET_CLIENT_VALIDATION_ERR}\n```Error_log: {e.errors()}```',
                parse_mode='Markdown'
            )

    async def delete_client_by_id(self, uid: str):
        response = requests.delete(
            f"{self.url}/clients/delete/{uid}"
        )

        await self.__get_response_data(response)

    async def update_client_by_id(self, uid: str, data: ClientDto) -> ClientSuccessResDto:
        response = requests.put(
            f"{self.url}/clients/update/{uid}", data
        )

        data = await self.__get_response_data(response)

        try:
            ClientSuccessResDto(**data)
            return data

        except ValueError as e:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f'{TextMsg.GET_CLIENT_VALIDATION_ERR}\n```Error_log: {e.errors()}```',
                parse_mode='Markdown'
            )

    async def create_client(self, message_id: int, data: any) -> ClientSuccessResDto:
        body = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "patronymic": data['patronymic'],
            "addresses": [{
                "city": data['city'],
                "address": data['address'],
            }],
            "phone": data['phone'],
            "about_client": data['about_client']
        }

        response = requests.post(
            f"{self.url}/clients/create", json=body
        )

        try:
            data = await self.__get_response_data(response)
            ClientSuccessResDto(**data)
            return data

        except ValueError as e:
            await self.bot.edit_message_text(
                TextMsg.CLIENT_ADD_ERROR(e),
                self.chat_id,
                message_id,
                reply_markup=add_client_reply_keyboard()
            )
