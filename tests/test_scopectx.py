import pytest

from scopectx import (Context, DuplicateContextException, MultiLevelContext,
                      NotInContextException)


@pytest.fixture()
def ctx():
    return Context()


@pytest.fixture()
def mlctx():
    return MultiLevelContext()


@pytest.fixture(params=[Context, MultiLevelContext])
def common_ctx(request):
    return request.param()


def test_not_in_context(common_ctx):
    with pytest.raises(NotInContextException):
        common_ctx['a'] = 5

    with pytest.raises(NotInContextException):
        common_ctx['a']


def test_key_error(common_ctx):
    with common_ctx:
        with pytest.raises(KeyError):
            common_ctx['a']


def test_same_level(common_ctx):
    with common_ctx:
        common_ctx['a'] = 5
        assert common_ctx['a'] == 5


def test_same_level_and_out(common_ctx):
    with common_ctx:
        common_ctx['a'] = 5
        assert common_ctx['a'] == 5

    with pytest.raises(NotInContextException):
        common_ctx['a']


def test_same_level_twice(common_ctx):
    with common_ctx:
        common_ctx['a'] = 5
        assert common_ctx['a'] == 5

    with common_ctx:
        with pytest.raises(KeyError):
            common_ctx['a']
        common_ctx['a'] = 10
        assert common_ctx['a'] == 10


def test_inside_functions(common_ctx):
    def f_check(a):
        assert common_ctx['a'] == a

    def f_set(a):
        common_ctx['a'] = a

    def f_set_and_check(a):
        f_set(a)
        f_check(a)

    with common_ctx:
        with pytest.raises(KeyError):
            f_check(5)

        f_set(10)
        f_check(10)
        f_set_and_check(15)
        f_check(15)
        assert common_ctx['a'] == 15


def test_duplicate_context_exception(common_ctx):
    with pytest.raises(DuplicateContextException):
        with common_ctx:
            with common_ctx:
                pass


def test_multiple_sets_and_gets_in_nested_contexts(ctx):
    def f_check(a):
        assert ctx['a'] == a

    def f_set(a):
        ctx['a'] = a

    def f_set_and_check(a):
        f_set(a)
        f_check(a)

    def f_with_nested_context():
        with ctx:
            with pytest.raises(KeyError):
                f_check(5)
            f_set_and_check(15)

    with ctx:
        f_set(10)
        f_with_nested_context()
        f_check(10)


def test_multiple_sets_and_gets_in_nested_multi_level_contexts(mlctx):
    def f_check(a):
        assert mlctx['a'] == a

    def f_set(a):
        mlctx['a'] = a

    def f_set_and_check(a):
        f_set(a)
        f_check(a)

    def f_with_nested_context():
        with mlctx:
            with pytest.raises(KeyError):
                mlctx['b']
            f_check(10)
            f_set_and_check(15)
            f_check(15)

    with mlctx:
        f_set(10)
        f_with_nested_context()
        f_check(10)
