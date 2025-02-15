from core import exceptions


def dd(
    *args, message: str | None = None, data: dict | list | None = None
) -> None:
    """
    Dump the given variables and then raise a SystemExit exception
    to stop execution of the script.
    """

    raise exceptions.BreakException(args, message=message, data=data)


def exclude_user(queryset, username="946593659"):
    return queryset.exclude(username=username)
