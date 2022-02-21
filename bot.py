from time import perf_counter

import requests
import lorem

URL = 'http://127.0.0.1:8000'


def create_post():
    random_title = lorem.sentence()
    random_text = lorem.paragraph()
    requests.post(f'{URL}/api/posts/',
                  headers={
                      'Content-Type': 'application/json'
                  },
                  json={
                      "title": random_title,
                      "text": random_text,
                      "user_id": 1
                  })


def main():
    for i in range(10):
        create_post()


if __name__ == '__main__':
    start = perf_counter()
    main()
    execution_time = perf_counter() - start
    print(f"Execution time: {execution_time:.4f} secs")
