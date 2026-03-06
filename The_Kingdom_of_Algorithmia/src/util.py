from collections.abc import Callable


def print_hex(hex: str, text: str, end="\n") -> None:
    r, g, b = tuple(int(hex[1:][i : i + 2], 16) for i in (0, 2, 4))
    escape = "\033[{};2;{};{};{}m".format(38, r, g, b)
    print(escape + text + "\033[0m", end=end)


def hexcolor_str(hex: str, text: str) -> str:
    r, g, b = tuple(int(hex[1:][i : i + 2], 16) for i in (0, 2, 4))
    escape = "\033[{};2;{};{};{}m".format(38, r, g, b)
    return escape + text + "\033[0m"


class Str:

    def __str__(self) -> str:
        return f"{type(self).__name__}({
            ', '.join(f'{n}={v}' for n, v in vars(self).items())
        })"

    __repr__ = __str__


def add_repr_str(
    cls: type | None = None, *, repr: bool = True, st: bool = False
) -> Callable[..., type] | type:
    def wrapper(cls: type) -> type:
        def f(self) -> str:
            return f"{type(self).__name__}({
                    ', '.join(f'{n}={v}' for n, v in vars(self).items())
            })"

        if repr:
            cls.__repr__ = f  # type: ignore
        if str:
            cls.__str__ = f  # type: ignore

        return cls

    if cls is None:
        return wrapper

    return wrapper(cls)
