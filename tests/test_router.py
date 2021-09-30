import pytest

from fusi import Router, RouterError


def test_router_add_route():
    router = Router()
    route = router.add_route(
        name="test",
        pattern="/test",
        handler=lambda: "Hello world",
        methods=["GET"]
    )
    assert route in router


def test_router_items():
    router = Router()
    route = router.add_route(
        name="test",
        pattern="/test",
        handler=lambda: "Hello world",
        methods=["GET"]
    )
    assert len(list(router.items())) == 1
    for name, route in router.items():
        assert name == "test"
        assert route is route


def test_router_match_name_no_match():
    router = Router()
    router.add_route(
        name="hello_world",
        pattern="/hello-world",
        handler=lambda: "Hello world",
        methods=["GET"],
    )
    match = router.match_name("foo")
    assert match is None


def test_router_match_name_with_router_name():
    router = Router(name="test")
    route = router.add_route(
        name="hello_world",
        pattern="/hello-world",
        handler=lambda: "Hello world",
        methods=["GET"],
    )
    match = router.match_name("test.hello_world")
    assert route is match


def test_router_match_name_with_router_name_and_prefix():
    router = Router(name="test", prefix="/api")
    route = router.add_route(
        name="hello_world",
        pattern="/hello-world",
        handler=lambda: "Hello world",
        methods=["GET"],
    )
    match = router.match_name("test.hello_world")
    assert route is match


def test_router_match_name_with_fallback():

    router = Router()
    router.add_route(
        name="test",
        pattern="/test",
        methods=["GET"],
        handler=lambda: "Hello world"
    )
    fallback = router.add_route(
        name="not_found",
        pattern="/404",
        methods=["GET"],
        handler=lambda: "Page not found",
    )
    match = router.match_name("does_not_exist", "not_found")
    assert match is fallback


def test_router_match_pattern_matches():
    router = Router()
    route = router.add_route(
        name="hello_world",
        pattern="/hello-world",
        handler=lambda: "Hello world",
        methods=["GET"],
    )
    match = router.match_pattern("/hello-world")
    assert match is route


def test_router_match_pattern_no_match():
    router = Router()
    route = router.add_route(
        name="hello_world",
        pattern="/hello-world",
        handler=lambda: "Hello world",
        methods=["GET"],
    )
    match = router.match_pattern("/ahoy-there")
    assert match is None


def test_router_match_pattern_no_match_with_fallback():
    router = Router()
    route = router.add_route(
        name="hello_world",
        pattern="/hello-world",
        handler=lambda: "Hello world",
        methods=["GET"],
    )
    fallback = router.add_route(
        name="fallback",
        pattern="/fallback",
        handler=lambda: "Fallback",
        methods=["GET"],
    )
    match = router.match_pattern("/does-not-exist", "fallback")
    assert match is fallback


def test_router_raises_router_error_with_bad_prefix():
    with pytest.raises(RouterError):
        router = Router(prefix="bad")


def test_router_len():
    router = Router()
    route = router.add_route(
        name="test",
        pattern="/test",
        handler=lambda: "Hello world",
        methods=["GET"]
    )
    route = router.add_route(
        name="test2",
        pattern="/test2",
        handler=lambda: "Hello world",
        methods=["GET"]
    )
    assert len(router) == 2


def test_router_raises_router_error_bad_name_type():
    router = Router()
    with pytest.raises(RouterError):
        router.add_route(name=1, pattern="/one", methods=["get"], handler=lambda: "Fail")


def test_router_raises_router_error_bad_pattern_type():
    router = Router()
    with pytest.raises(RouterError):
        router.add_route(name="ok", pattern=1, methods=["get"], handler=lambda: "Fail")


def test_router_raises_router_error_bad_handler_type():
    router = Router()
    with pytest.raises(RouterError):
        router.add_route(name="ok", pattern="/ok", methods=["get"], handler="fail")


def test_router_raises_router_error_pattern_no_slash():
    router = Router()
    with pytest.raises(RouterError):
        router.add_route(name="fail", pattern="fail", methods=["get"], handler=lambda: "Test")


def test_router_raises_router_error_duplicate_name():
    router = Router()
    router.add_route(name="ok", pattern="/ok", methods=["get"], handler=lambda: "Test")
    with pytest.raises(RouterError):
        router.add_route(name="ok", pattern="/ok", methods=["get"], handler=lambda: "Test")

# TODO - Subclass Router and test methods

