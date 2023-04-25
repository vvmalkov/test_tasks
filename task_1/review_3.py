def some_useful_function_to_be_imported():
    pass


def some_heavy_app_initialization():
    pass


if __name__ == '__main__':
    app = some_heavy_app_initialization()
    app.run()