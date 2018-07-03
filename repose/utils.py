def make_thinner(interval):
    """
    Return a thinner function for the given interval.

    The function should be called with sequential values;
    if the value should be used, the function will return True,
    if ignored, False.

    :param interval: Interval; whatever makes sense for the values passed in.
    :return: Thinner function.
    """
    last = None

    def thinner(curr):
        nonlocal last
        if last is None or curr - last >= interval:
            last = curr
            return True
        else:
            return False

    return thinner
