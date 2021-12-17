from util import load_pkl, save_pkl


def convert__type2_doc():
    for i in range(10):
        file_path = "unzipdata/body" + str(i) + ".pkl"
        items = load_pkl(file_path)
        for item in items:
            item["_type"] = '_doc'
        save_pkl(file_path, items)
        print(str(i))

def print_file():
    for i in range(10):
        file_path = "unzipdata/body" + str(i) + ".pkl"
        items = load_pkl(file_path)
        for item in items:
            print(item)

if __name__ == '__main__':
    convert__type2_doc()
    # print_file()
