from visset.utils import self_factory, singleton


@singleton
class Connection:

    def __init__(self, host: str = ..., database: str = ..., user: str = ..., password: str = ...) -> None:
        self.host = host
        self.database = database
        self.user = user
        self.password = password


class SubTypeConnection(Connection):
    ...


@self_factory
class Session:

    def __init__(self, id: int) -> None:
        self.id = id


class SubTypeSession(Session):
    ...


def test_singleton():
    connection_1 = Connection(host = 'localhost')
    connection_2 = Connection(host = 'localhost')
    assert connection_1 is connection_2


def test_sub_type_singleton():
    connection_1 = SubTypeConnection(host = 'localhost')
    connection_2 = Connection(host = 'localhost')
    assert connection_1 is connection_2


def test_self_factory_with_args():
    session_1 = Session(id = 1)
    session_2 = Session(id = 1)
    session_3 = Session(id = 3)
    assert session_1 is session_2
    assert session_1 is not session_3


def test_self_factory_with_kwargs():
    session_1 = Session(4)
    session_2 = Session(4)
    session_3 = Session(5)
    assert session_1 is session_2
    assert session_1 is not session_3


def test_sub_type_self_factory():
    session_1 = SubTypeSession(id = 6)
    session_2 = Session(id = 6)
    assert session_1 is session_2
    assert isinstance(session_1, SubTypeSession)
    assert isinstance(session_2, SubTypeSession)
    assert session_1.id == 6
