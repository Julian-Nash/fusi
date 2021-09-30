from fusi import Route


def test_route_attrs():
    route = Route(name="test", pattern="/test", methods=["get"], handler=lambda: "Test")
    assert route.name == "test"
    assert route.pattern == "/test"
    assert route.methods == ("GET", )
    assert route.handler() == "Test"


def test_route_repr():

    def some_handler():  # pragma: no cover
        pass

    route = Route(name="test", pattern="/test", methods=["get"], handler=some_handler)
    r = repr(route)
    assert r == "Route(name='test', pattern='/test', handler='some_handler' methods=('GET',))"
