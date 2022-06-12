from acervo.utils import self_factory, singleton

@singleton
class Connection:
    
    def __init__(self, host: str = ..., database: str = ..., user: str = ..., password: str = ...) -> None:
        self.host = host
        self.database = database
        self.user = user
        self.password = password
    

@self_factory
class Session:

    def __init__(self, id: int) -> None:
        self.id = id


def test_singleton():
    connection_1 = Connection(host = 'localhost')
    connection_2 = Connection(host = 'localhost')
    assert connection_1 is connection_2


def test_session_with_args():
    session_1 = Session(id = 1)
    session_2 = Session(id = 1)
    session_3 = Session(id = 3)
    assert session_1 is session_2
    assert session_1 is not session_3


def test_session_with_kwargs():
    session_1 = Session(1)
    session_2 = Session(1)
    session_3 = Session(3)
    assert session_1 is session_2
    assert session_1 is not session_3