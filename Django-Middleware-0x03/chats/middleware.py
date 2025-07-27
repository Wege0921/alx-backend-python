# chats/middleware.py
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        with open('requests.log', 'a') as log_file:
            log_file.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")
        response = self.get_response(request)
        return response

from datetime import datetime, time
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current time
        current_time = datetime.now().time()

        # Define allowed time range: 6 AM to 9 PM
        start_time = time(6, 0, 0)
        end_time = time(21, 0, 0)

        # If path contains 'chat' and current time is outside allowed range
        if 'chat' in request.path.lower() and not (start_time <= current_time <= end_time):
            return HttpResponseForbidden("Access to chat is restricted outside 6AM to 9PM.")

        # Otherwise, continue processing
        return self.get_response(request)

