from heapq import nlargest
import random
from operator import itemgetter

dict = {
    "246862123328733186": 31,
    "253059354331316224": 32
}


def get_top_dict(dictionary, num=10000000000000000, return_type="full"):
    topx = {k: v for k, v in sorted(dictionary.items(), key=itemgetter(1), reverse=True)[:num]}

    return_list = []
    for key in topx:
        return_list.append((key, dictionary[key]))

    if return_type == "raw":
        return return_list[0][0]

    elif return_type == "full":
        return return_list

    else:
        raise TypeError(f"return_type of {return_type} is not valid")

print(get_top_dict(dict, 1))
print(get_top_dict(dict, 1))
print(get_top_dict(dict, 1))

dict = {
    "246862123328733186": 32,
    "253059354331316224": 32
}

print(get_top_dict(dict, 1, "raw"))
print(get_top_dict(dict, 1, "raw"))
print(get_top_dict(dict, 1, "f"))

def random_data(num=500):
	return_data_dict = {}
	for _ in range(num):
		return_data_dict[str(random.randint(100000000000000000, 999999999999999999))] = random.randint(1, 1000)

	return return_data_dict



print(get_top_dict(random_data(20000), 100000))
