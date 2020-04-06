client_data = "12.12,325.40,83.71,15.52,38.63,76.51,193.03,258.50,258.70#13.11,331.50,83.46,16.38,40.52,79.33,196.36,258.30,258.50#14.08,337.10,83.63,17.21,42.36,85.14,211.88,258.70,258.50#15.10,342.70,83.08,18.18,44.35,89.91,221.76,258.70,258.60"
groups = client_data.split("#")
for index, group in enumerate(groups):
    print("info {} of group {}".format(index, group))
    values = [float(x) for x in group.split(",")]
    print(values)
    # if values[0] == "data":


def hello(first, second):
    """ Description
    :type first:
    :param first:

    :type second:
    :param second:

    :raises:

    :rtype:
    """
    pass
