def request_handler(request):
    local_file = open(request.params['file_path'])
    return Response(local_file.read())