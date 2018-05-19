def once(a_func):
    """Wrapper to reuse value returned with a first use on all future calls"""

    counter = 0
    output = 0  # may be initiated to anything

    def wrapper():
        nonlocal counter, output
        if counter < 1:
            output = a_func()
        else:
            counter += 1
        return output

    return wrapper


