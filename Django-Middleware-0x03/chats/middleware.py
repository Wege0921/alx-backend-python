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

import time
from django.http import HttpResponseTooManyRequests
from collections import defaultdict

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Track requests: {IP: [timestamps]}
        self.request_logs = defaultdict(list)

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Only track POST requests to chat endpoints
        if request.method == 'POST' and 'chat' in request.path.lower():
            current_time = time.time()
            window_start = current_time - 60  # 1-minute window

            # Remove old timestamps
            self.request_logs[ip] = [
                timestamp for timestamp in self.request_logs[ip]
                if timestamp > window_start
            ]

            # Block if more than 5 messages in the last 60 seconds
            if len(self.request_logs[ip]) >= 5:
                return HttpResponseTooManyRequests("Rate limit exceeded: Only 5 messages per minute allowed.")

            # Otherwise, log the current request
            self.request_logs[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        # Get IP from request headers
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


