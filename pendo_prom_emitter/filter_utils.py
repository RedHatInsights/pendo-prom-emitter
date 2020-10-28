def operation_in(value, test):
    """Check if value is in the test list."""
    found = False
    for test_in in test:
        if test_in in value:
            found = True
            break
    return found


def operation_equal(value, test):
    """Compare if value is equal to test."""
    return value == test


def operation_startswith(value, test):
    """Check if value start swith test."""
    return value.startswith(test)
