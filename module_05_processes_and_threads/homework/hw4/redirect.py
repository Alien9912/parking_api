"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""

from types import TracebackType
from typing import Type, Literal, IO, Optional
import sys
import traceback


class Redirect:
    def __init__(self, stdout: Optional[IO] = None, stderr: Optional[IO] = None) -> None:
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
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
    ) -> Optional[Literal[True]]:
        if exc_type is not None and self.stderr is not None:
            traceback.print_exception(exc_type, exc_val, exc_tb, file=self.stderr)
            sys.stdout = self.old_stdout
            sys.stderr = self.old_stderr
            return True
        else:
            sys.stdout = self.old_stdout
            sys.stderr = self.old_stderr
            return None