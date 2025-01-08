import time
import itertools
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.cache import caches

class Command(BaseCommand):
    help = "Find the optimal timeout and max_connections for the /api/products/filter/ endpoint, testing different MAX_ENTRIES."

    def handle(self, *args, **kwargs):
        socket_timeout_options = [200, 500]
        connect_timeout_options = [200, 500]
        timeout_options = [20, 100, 180, 300, 600]
        max_connections_options = [ 20, 30]
        max_entries_options = [1000, 2000] 
        url = f"{settings.VERCEL_DOMAIN}/api/products/filter/"
        
        param_combinations = itertools.product(
            socket_timeout_options,
            connect_timeout_options,
            timeout_options,
            max_connections_options,
            max_entries_options  # Adding MAX_ENTRIES combinations
        )

        best_params = None
        best_time = float('inf')
        results = {}
        for socket_timeout, connect_timeout, timeout, max_connections, max_entries in param_combinations:
            cache_params = {
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                    'CONNECTION_POOL_KWARGS': {
                        'max_connections': max_connections,
                        'retry_on_timeout': True,
                    },
                    'IGNORE_EXCEPTIONS': True,
                    'SOCKET_CONNECT_TIMEOUT': connect_timeout,
                    'SOCKET_TIMEOUT': socket_timeout,
                    'MAX_ENTRIES': max_entries,  # Setting the value of MAX_ENTRIES here
                    'CONNECTION_POOL_CLASS': 'redis.connection.ConnectionPool',
                },
                'KEY_PREFIX': 'filter_api',
                'TIMEOUT': 20,
            }

            settings.CACHES['default'].update(cache_params)
            cache = caches['default']
            cache.clear()

            start_time = time.time()
            elapsed_time = None 
            response = None  # Initialize response to avoid UnboundLocalError
            try:
                response = requests.get(url, params={
                    'category': '',
                    'collection': '',
                    'ordering': '',
                    'page': 1,
                    'page_size': 8
                }, timeout=(connect_timeout, socket_timeout)) 
                
                if response.status_code == 200:
                    elapsed_time = time.time() - start_time
                    results[(socket_timeout, connect_timeout, timeout, max_connections, max_entries)] = elapsed_time
                    self.stdout.write(f"Tested params: connect_timeout={connect_timeout}, "
                                      f"socket_timeout={socket_timeout}, timeout={timeout}, "
                                      f"max_connections={max_connections}, max_entries={max_entries} => Load time: {elapsed_time:.2f}s")
                else:
                    self.stdout.write(f"Request failed with status code {response.status_code} for params: "
                                      f"connect_timeout={connect_timeout}, socket_timeout={socket_timeout}, "
                                      f"timeout={timeout}, max_connections={max_connections}, max_entries={max_entries}")
            except requests.exceptions.RequestException as e:
                self.stdout.write(f"Error with params: connect_timeout={connect_timeout}, "
                                f"socket_timeout={socket_timeout}, timeout={timeout}, "
                                f"max_connections={max_connections} => {e}")
                
                if response and response.status_code == 504:  # Check if response is not None before accessing
                    self.stdout.write(f"Response Headers: {response.headers}")
                    self.stdout.write(f"Response Body: {response.text}")

            if elapsed_time is not None and elapsed_time < best_time:
                best_time = elapsed_time
                best_params = (socket_timeout, connect_timeout, timeout, max_connections, max_entries)

        if best_params:
            self.stdout.write("\nOptimal Parameters:")
            self.stdout.write(f"connect_timeout={best_params[1]}, socket_timeout={best_params[0]}, "
                              f"timeout={best_params[2]}, max_connections={best_params[3]}, max_entries={best_params[4]} => "
                              f"Best Load time: {best_time:.2f}s")
        else:
            self.stdout.write("No successful requests were made.")
