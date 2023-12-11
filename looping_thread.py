from threading import Event, Thread
from typing import Any, Callable, Iterable, Mapping


class LoopingThread:
    def __init__(self,
                 target: Callable,
                 wait: float = 0,
                 args: Iterable = (),
                 kwargs: Mapping[str, Any] = {}) -> None:
        self.thread = Thread(target=self.run)
        self.target = target
        self.wait = wait
        self.args = args
        self.kwargs = kwargs
        self.stop_event = Event()

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self.stop_event.set()
        self.thread.join()

    def is_stopped(self) -> bool:
        return self.stop_event.is_set()

    def run(self) -> None:
        while not self.stop_event.wait(self.wait):
            self.target(*self.args, **self.kwargs)


if __name__ == '__main__':
    loop = LoopingThread(target=print, wait=0.5, args=['LOOP: Hello'])
    print('START')
    loop.start()
    user_input = input()
    loop.stop()
    print('STOPPED')
    print(f'Input: {user_input}')
