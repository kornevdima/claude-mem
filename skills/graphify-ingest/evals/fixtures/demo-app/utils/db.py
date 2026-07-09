import contextlib

class FakeConnection:
    def execute(self, sql, params=None): pass
    def query_one(self, sql, params=None): return {}

@contextlib.contextmanager
def get_connection():
    yield FakeConnection()
