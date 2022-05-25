import json
import random
import secrets
import names
import aiohttp
import asyncio

from time import time
from conf import users_amount, SIGNUP_URL, GET_TOKEN

requests_amount = []


class User:
    def __init__(self, username):
        self.username = username
        self.email = f'{username}@email.com'
        self.password = secrets.token_hex(random.randint(15, 20))
        self.headers = {'Content-Type': 'application/json'}

    async def register(self, session, signup_url):
        data = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'password2': self.password,
        }
        async with session.post(signup_url, headers=self.headers, data=json.dumps(data)) as result_awaitable:
            await result_awaitable.json()
            requests_amount.append(None)

    async def token(self, session, token_url):
        data = {
            "username": self.username,
            "password": self.password,
        }
        async with session.post(token_url, headers=self.headers, data=json.dumps(data)) as result_awaitable:
            await result_awaitable.json()
            requests_amount.append(None)


async def tasks_factory(users, task, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        tasks = [task(user, *args, **kwargs, session=session) for user in users]
        await asyncio.gather(*tasks)


async def main():
    users = [User(names.get_first_name()) for i in range(users_amount)]
    await tasks_factory(users=users, task=User.register, signup_url=SIGNUP_URL)
    await tasks_factory(users=users, task=User.token, token_url=GET_TOKEN)


if __name__ == '__main__':
    start = time()
    asyncio.run(main())
    print(f'It costed {time() - start} seconds to make {len(requests_amount)} requests')
