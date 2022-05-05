
class UserMiddleware():
    # the init initialises the method and is only run one time - the init is required
    def __init__(self, get_response):
        self.get_response = get_response
    # the call method s used each time that someone tries to access a page - the call is required
    def __call__(self, request):



        response = self.get_response(request)
        # at the end the response is returned
        return response