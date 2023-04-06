def load_modules(path, globals):
    import pkgutil
    import inspect
    for loader, name, _ in pkgutil.walk_packages(path):
        module = loader.find_module(name).load_module(name)

        for name, value in inspect.getmembers(module):
            if name.startswith('__'):
                continue

            globals[name] = value