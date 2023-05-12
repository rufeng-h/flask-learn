import dataclasses
import typing


class Serializable:
    _exclude_fields = ()

    def __init__(self, *args, **kwargs):
        """
        定义*args，**kwargs参数，接受任何参数
        """
        self.__dict__.update(kwargs)

    def keys(self) -> typing.Iterable[str]:
        """
        返回所有需要序列化的字段
        忽略受保护的字段（以_开头）
        忽略为None的字段
        忽略指定字段，_exclude_fields
        """
        print("keys")
        return filter(
            lambda k: k not in self._exclude_fields and not k.startswith('_') and self.__dict__[k] is not None,
            self.__dict__)

    def __getitem__(self, key) -> typing.Any:
        print("__getitem__" + str(key))
        return getattr(self, key)


"""
dataclass可有可无
"""


@dataclasses.dataclass
class ApiResponse(Serializable):
    code: int
    message: str
    data: typing.Any

    @classmethod
    def success(cls, data=None):
        if data:
            return cls(code=200, message='操作成功', data=data)
        return cls(code=200, message='操作成功', data=None)

    @classmethod
    def server_error(cls):
        return cls(code=500, message='服务器异常', data=None)


if __name__ == '__main__':
    response = ApiResponse.success()
    # print(dict(response))
    # print(ApiResponse.__dict__.get('__annotations__', []))
    # print(response)

    for k, v in response:
        print(k, v)
