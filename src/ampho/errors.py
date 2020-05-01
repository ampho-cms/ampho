"""Ampho Errors
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AmphoError(Exception):
    """Base Ampho error
    """


class BundleError(AmphoError):
    """Bundle's module is not found
    """

    def __init__(self, name: str):
        """Init
        """
        super().__init__()
        self._name = name


class BundleImportError(BundleError):
    """Error while importing bundle module
    """

    def __str__(self) -> str:
        return f"Bundle's module '{self._name}' cannot be imported"


class BundleAlreadyImportedError(BundleError):
    """Error while importing bundle module more than once
    """

    def __str__(self) -> str:
        return f"Bundle's module '{self._name}' is already imported"


class BundleNotRegisteredError(BundleError):
    """Bundle with the specified name is not registered
    """

    def __str__(self) -> str:
        return f"Bundle '{self._name}' is not registered"


class BundleAlreadyRegisteredError(BundleError):
    """Bundle with the same name is already registered
    """

    def __str__(self) -> str:
        return f"Bundle '{self._name}' is already registered"


class BundleNotLoadedError(BundleError):
    """Bundle is not loaded
    """

    def __str__(self) -> str:
        return f"Bundle '{self._name}' is not loaded"


class BundleAlreadyLoadedError(BundleError):
    """Bundle is not loaded
    """

    def __str__(self) -> str:
        return f"Bundle '{self._name}' is already loaded"


class BundleCircularDependencyError(BundleError):
    """Circular dependency detected while loading a bundle
    """

    def __init__(self, name: str, loading_stack: list):
        """Init
        """
        super().__init__(name)

        self._stack = loading_stack

    def __str__(self) -> str:
        return f"Bundle '{self._name}' is already being loaded. " \
               "Check your setup against circular dependencies. " \
               f"Loading stack content: {self._stack}"
