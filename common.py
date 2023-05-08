import dataclasses
import typing


@dataclasses.dataclass
class ApiResponse:
    code: int
    message: str
    data: typing.Any

    @classmethod
    def success(cls, data):
        return cls(200, '操作成功', data)

    @classmethod
    def server_error(cls):
        return cls(500, '服务器异常', None)
