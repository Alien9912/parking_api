"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""

from types import TracebackType
from typing import Type, Literal, IO
import sys


class Redirect:
    def __init__(self, stdout: IO = None, stderr: IO = None) -> None:
        self.stdout = stdout
        self.stderr = stderr
        self.old_stdout = None
        self.old_stderr = None

    def __enter__(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        if self.stdout is not None:
            sys.stdout = self.stdout
        if self.stderr is not None:
            sys.stderr = self.stderr

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        return None