from typing import Optional, Dict, List, Union, Callable, Sequence
from functools import lru_cache

from .route import Route


class RouterError(Exception):
    """ Raised when an illegal operation is encountered when configuring
    or adding a route to a Router
    """


class Router:

    def __init__(self, name: Optional[str] = None, prefix: Optional[str] = None):
        """ A reversible web application router.

        Args:
            name (str): The name of the router (Optional)
            prefix (str): A prefix to prepend to all patterns (Optional)

        The `name` parameter is prepended to the route name.
        >>> from fusi import Router
        >>> router = Router(name="public")
        >>> route = router.add_route(name="home", pattern="/", methods=["GET"], handler=lambda: "Hello world")
        >>> route.name
        'public.home'

        The `prefix` parameter is prepended to the route pattern.
        >>> router = Router(name="rest_api", prefix="/v1")
        >>> route = router.add_route(name="users", pattern="/users", methods=["GET"], handler=lambda: [1, 2, 3])
        >>> route.pattern
        '/v1/users'

        Note - `prefix` must start with a leading slash
        >>> router = Router(name="rest_api", prefix="v1")
        Traceback (most recent call last):
          File "<input>", line 1, in <module>
          File "/Users/julian/Projects/python_packages/fusi/fusi/router.py", line 28, in __init__
        fusi.router.RouterError: Parameter 'prefix' must start with a leading slash '/' not 'v1'

        """
        if prefix and not prefix.startswith("/"):
            raise RouterError(f"Parameter 'prefix' must start with a leading slash '/' not '{prefix}'")
        self._name = name
        self._prefix = prefix
        self._routes: Dict[str, Route] = {}

    def __contains__(self, item):
        return item in self.routes

    def __len__(self):
        return len(self._routes)

    @property
    def name(self):
        return self._name

    @property
    def prefix(self):
        return self._prefix

    @property
    def routes(self) -> List[Route]:
        """ Returns a list of all routes added to the router """
        return list(self._routes.values())

    def items(self):
        """ Yields the routers routes (name: str, route: Route) """
        for name, route in self._routes.items():
            yield name, route

    def match_name(self, name: str, fallback: Optional[str] = None) -> Union[Route, None]:
        """ Match a route by name. Returns a Route object or None
        An optional `fallback` parameter can be used as a route name to fall back to.
        """
        try:
            return self._routes[name]
        except KeyError:
            if fallback:
                return self.match_name(fallback)
        return None

    def is_pattern_match(self, pattern: str, route: Route) -> bool:
        """ Basic pattern match. Override this method.
        This method is called from `match_pattern` and is used to perform the actual
        pattern match, returning either True if the pattern matches, otherwise False.
        It receives a pattern (the raw URL path) and a Route object.
        """
        return pattern == route.pattern

    @lru_cache
    def match_pattern(self, pattern: str, fallback: Optional[str] = None) -> Union[Route, None]:
        """ Match a route by pattern. Returns a Route object or None.
        An optional `fallback` parameter can be used as a route name to fall back to.
        Note - This method utilises the `lru_cache` decorator & `lru_cache` defaults.
        """
        for route in self.routes:
            if self.is_pattern_match(pattern, route):
                return route
        if fallback:
            return self.match_name(fallback)
        return None

    def prepare_route_name(self, name: str) -> str:
        """ Called from `add_route`, this method is used to prepare the route
        name before being passed to `check_route_name`.
        """
        return self.name + "." + name if self.name else name

    def check_route_name(self, name: str) -> bool:
        """ Called from `add_route`, this method is used to check the name
        of the route before adding to the Router.
        Use of the `RouterError` exception is advised here to catch invalid/illegal route names.
        """
        return True

    def prepare_route_pattern(self, pattern: str) -> str:
        """ Called from `add_route`, this method is used to prepare the pattern
        name before being passed to `check_route_pattern`.
        Use of the `RouterError` exception is advised here to catch invalid/illegal route patterns.
        """
        return self.prefix + pattern if self.prefix else pattern

    def check_route_pattern(self, pattern: str) -> bool:
        """ Called from `add_route`, this method is used to check the pattern
        of the route before adding to the Router.
        """
        if not pattern.startswith("/"):
            raise RouterError("'pattern' must start with a '/'")
        return True

    def prepare_route_handler(self, handler: Callable) -> Callable:
        """ This method can be overridden to perform and checks or mutations
        on the handler before adding it to the Router.
        """
        return handler

    def add_route(
            self,
            name: str,
            pattern: str,
            handler: Callable,
            methods: Sequence[str]
    ) -> Route:
        """ Add a Route to the Router

        Args:
            name (str): The name of the route
            pattern (str): The pattern of the route
            handler (Callable): A callable to bind to the route
            methods (Sequence[str]): A sequence of request methods ("GET", "POST") etc...
        Returns:
            The Route object
        """

        if not isinstance(name, str):
            raise RouterError(f"parameter 'name' must be a string, not '{type(pattern)}'")

        if not isinstance(pattern, str):
            raise RouterError(f"parameter 'pattern' must be a string, not '{type(pattern)}'")

        if not callable(handler):
            raise RouterError(f"parameter 'handler' must be callable, not '{type(handler)}'")

        route_name = self.prepare_route_name(name)
        if route_name in self._routes:
            raise RouterError(f"Route with name '{name}' already exists")

        route_pattern = self.prepare_route_pattern(pattern)

        self.check_route_name(route_name)
        self.check_route_pattern(route_pattern)
        route_handler = self.prepare_route_handler(handler)

        route = Route(name=route_name, pattern=route_pattern, handler=route_handler, methods=methods)

        self._routes[route_name] = route

        return route
