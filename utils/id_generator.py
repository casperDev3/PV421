from typing import Generator

user_id_counter = 1

def user_id_generator() -> Generator[int, None, None]:
    global user_id_counter
    while True:
        yield user_id_counter
        user_id_counter += 1

id_gen = user_id_generator()