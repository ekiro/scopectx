import pytest

from scopectx import Context, DuplicateContextException, NotInContextException


@pytest.fixture()
def ctx():
    return Context()


def test_not_in_context(ctx):
    with pytest.raises(NotInContextException):
        ctx['a'] = 5

    with pytest.raises(NotInContextException):
        ctx['a']


def test_key_error(ctx):
    with ctx:
        with pytest.raises(KeyError):
            ctx['a']


def test_same_level(ctx):
    with ctx:
        ctx['a'] = 5
        assert ctx['a'] == 5


def test_same_level_and_out(ctx):
    with ctx:
        ctx['a'] = 5
        assert ctx['a'] == 5

    with pytest.raises(NotInContextException):
        ctx['a']


def test_same_level_twice(ctx):
    with ctx:
        ctx['a'] = 5
        assert ctx['a'] == 5

    with ctx:
        with pytest.raises(KeyError):
            ctx['a']
        ctx['a'] = 10
        assert ctx['a'] == 10


def test_inside_functions(ctx):
    def f_check(a):
        assert ctx['a'] == a

    def f_set(a):
        ctx['a'] = a

    def f_set_and_check(a):
        f_set(a)
        f_check(a)

    with ctx:
        with pytest.raises(KeyError):
            f_check(5)

        f_set(10)
        f_check(10)
        f_set_and_check(15)
        f_check(15)
        assert ctx['a'] == 15


def test_duplicate_context_exception(ctx):
    with pytest.raises(DuplicateContextException):
        with ctx:
            with ctx:
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
            f_set_and_check(15)

    with ctx:
        f_set(10)
        f_with_nested_context()
        f_check(10)
