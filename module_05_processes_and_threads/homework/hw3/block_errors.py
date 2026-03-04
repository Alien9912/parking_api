"""
Реализуйте контекстный менеджер, который будет игнорировать переданные типы исключений, возникающие внутри блока with.
Если выкидывается неожидаемый тип исключения, то он прокидывается выше.
"""

from typing import Collection, Type, Literal
from types import TracebackType


class BlockErrors:
    def __init__(self, errors: Collection) -> None:
        self.errors = errors

    def __enter__(self) -> None:
        pass

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        if exc_type is None:
            return None
        for err in self.errors:
            if issubclass(exc_type, err):
                return True
        return None