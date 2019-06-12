import sys
if __name__ == "__main__":
    class_name = sys.argv[1]
    module_name = "test_plugins." + class_name
    del sys.argv[1]
    new_module = __import__(module_name)