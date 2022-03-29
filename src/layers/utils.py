from functools import wraps

def initialize_wrapper(name):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            print(f"##### Start Initialization of {name} #####")
            func(*args, **kwargs)
            print(f"##### Done Initialization of {name} #####")
        return decorator
    return wrapper