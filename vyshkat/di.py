class DependencyError(LookupError):
    pass
# если что под рецептом имеется в виду, что условно кладовщик смотрит рецепт парка
# видит, что для него нужен техосмотр и рулон, делает их по рецептам, собирает парк и отдает мне

class Container:

    def __init__(self):
        self._factories = {} # книга рецептов
        self._is_singleton = {} # режим рецепта (тру фолс)
        self._singletons = {} # полка готового
        self._resolving = [] # собираем щас

# далее записываем рецепт, если key это что делает, то фактори как делает
    def register_singleton(self, key, factory): # сделать один раз, дальше отдавать его же
        self._register(key, factory, True)

    def register_transient(self, key, factory): # каждый раз делать новый
        self._register(key, factory, False)

    def register_instance(self, key, instance):
        def factory(container):
            return instance
        self.register_singleton(key, factory)

    def _register(self, key, factory, singleton):
        self._factories[key] = factory
        self._is_singleton[key] = singleton
        if key in self._singletons:
            del self._singletons[key]

    def resolve(self, key): # уже делали пс берем и ничего не создаем
        if key in self._singletons:
            return self._singletons[key]

        if key not in self._factories: # если рецепта нет, то кик
            raise DependencyError("Зависимость не зарегистрирована: " + key.__name__)
        # уже собираем этот класс => рецепты ссылаются друг на друга
        if key in self._resolving:
            chain = ""
            for k in self._resolving:
                chain = chain + k.__name__ + " -> "
            chain = chain + key.__name__
            raise DependencyError("Циклическая зависимость: " + chain)
        # готовим по рецепту
        self._resolving.append(key)
        try:
            factory = self._factories[key]
            instance = factory(self)
        finally:
            self._resolving.pop()
        # кладем на полку чтобы в след раз отдать этот же
        if self._is_singleton[key]:
            self._singletons[key] = instance

        return instance