import dataclasses
import typing


class Serializable:
    exclude_fields = ()

    def keys(self) -> typing.Iterable[str]:
        return filter(lambda k: k not in self.exclude_fields and not k.startswith('_') and self.__dict__[k] is not None,
                      self.__dict__)

    def __getitem__(self, key) -> typing.Any:
        return getattr(self, key)


@dataclasses.dataclass
class ApiResponse(Serializable):
    code: int
    message: str
    data: typing.Any

    @classmethod
    def success(cls, data=None):
        if data:
            return cls(200, '操作成功', data)
        return cls(200, '操作成功', None)

    @classmethod
    def server_error(cls):
        return cls(500, '服务器异常', None)

    def __getitem__(self, key):
        return getattr(self, key)
