def request_handler(request):
    try:
        with open(request.params['file_path'], 'r') as local_file:
            file_contents = local_file.read()
        response = Response(file_contents)
    except IOError as e:
        response = Response('Error: Could not open file', status=500)
    return response