
def func(data):
    """
    This function extracts the instance types with the price for each region, 
    returning them into a dictionary.
    """

    last = dict()
    for item in data:
        d = dict()
        for instanceType in item['instanceTypes']:
            sizes = instanceType['sizes']
            for size in sizes:
                instance_type = size['size']
                price = size['valueColumns'][0]['prices']['USD']
                d.update({instance_type: price})
        last.update({item['region']: d})
    return last
