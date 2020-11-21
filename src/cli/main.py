from pycli.tasks import pull_transform_push


class OltpCLIHandler:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def validate_kwargs(kwargs):
        pass


import sys
from .classmodule import MyClass
from .funcmodule import my_function


def main():
    print("in main")
    args = sys.argv[1:]
    print("count of args :: {}".format(len(args)))
    for arg in args:
        print("passed argument :: {}".format(arg))

    kwargs = {"output_topic": "aa", "input_topic": topic, "index": 1, "value": value}
    info["topics"].append(kwargs)
    pull_transform_push.delay(**kwargs)

    my_object = MyClass("Thomas")
    my_object.say_name()


if __name__ == "__main__":
    main()
