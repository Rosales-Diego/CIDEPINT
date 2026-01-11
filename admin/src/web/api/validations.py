
def validate_positive_int(*args):
    for value in args:
        assert value > 0, "Value must be greater than 0."
        assert isinstance(value, int), "Value must be an integer."
    return True
    