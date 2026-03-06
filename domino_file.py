import os
import typing

from flytekit.types.file import FileExt
from flytekit.types.file.file import FlyteFile, noop

# hash: 10546178329c

class DominoFile(FlyteFile):
    """Thin wrapper on FlyteFile that automatically sets ``file_extension``
    to match the subscript type.

    ``DominoFile["csv"]`` behaves identically to ``FlyteFile["csv"]`` for
    format / type-checking purposes, but additionally sets
    ``file_extension="csv"`` so that flytecopilot writes the blob with the
    correct extension during the download phase.

    Usage::

        @task
        def produce() -> DominoFile["csv"]:
            return DominoFile["csv"](path="/tmp/data.csv")

        @task
        def consume(f: DominoFile["csv"]):
            ...
    """

    @classmethod
    def extension(cls) -> str:
        return ""

    def __class_getitem__(
        cls, item: typing.Union[str, typing.Type]
    ) -> typing.Type["DominoFile"]:
        if item is None:
            return cls

        item_string = FileExt.check_and_convert_to_str(item)
        item_string = item_string.strip().lstrip("~").lstrip(".")
        if item == "":
            return cls

        class _DominoSpecificFormatClass(DominoFile):
            __origin__ = FlyteFile

            class AttributeHider:
                def __get__(self, instance, owner):
                    raise AttributeError(
                        "Hiding __class_getitem__ so mashumaro deserializes correctly."
                    )

            __class_getitem__ = AttributeHider()  # type: ignore

            @classmethod
            def extension(cls) -> str:
                return item_string

        return _DominoSpecificFormatClass

    def __init__(
        self,
        path: typing.Union[str, os.PathLike],
        downloader: typing.Callable = noop,
        remote_path: typing.Optional[typing.Union[os.PathLike, str, bool]] = None,
        metadata: typing.Optional[dict[str, str]] = None,
        file_extension: str = "",
    ):
        if not file_extension:
            file_extension = type(self).extension()
        super().__init__(
            path=path,
            downloader=downloader,
            remote_path=remote_path,
            metadata=metadata,
            file_extension=file_extension,
        )
