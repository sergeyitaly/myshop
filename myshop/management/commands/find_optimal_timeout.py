import time
import itertools
from django.core.cache import caches
from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import Product

class Command(BaseCommand):
    help = "Find the optimal Redis cache parameters for product loading."

    def handle(self, *args, **kwargs):
        # Define parameter ranges to test
        max_connections_options = [2, 6, 10, 20, 30, 40, 50, 100, 200, 300]
        socket_timeout_options = [1, 2, 5, 10, 20]
        max_entries_options = [10, 50, 100, 500, 1000]
        timeout_options = [10, 20, 30, 60, 120]
        
        # Generate all possible combinations of parameters to test
        param_combinations = itertools.product(
            max_connections_options, 
            socket_timeout_options, 
            max_entries_options, 
            timeout_options
        )

        best_params = None
        best_time = float('inf')
        results = {}

        # Test each combination
        for max_connections, socket_timeout, max_entries, cache_timeout in param_combinations:
            # Set up cache params for this combination
            cache_params = {
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                    'CONNECTION_POOL_KWARGS': {
                        'max_connections': max_connections,
                        'retry_on_timeout': True,
                    },
                    'IGNORE_EXCEPTIONS': True,  # Avoid crashes when Redis is down
                    'SOCKET_CONNECT_TIMEOUT': socket_timeout,
                    'SOCKET_TIMEOUT': socket_timeout,
                    'MAX_ENTRIES': max_entries,
                    'CONNECTION_POOL_CLASS': 'redis.connection.ConnectionPool',
                },
                'KEY_PREFIX': 'product',  # Use a specific prefix for product-related cache
                'TIMEOUT': cache_timeout,  # Test with the dynamic timeout
            }

            # Manually update the CACHES settings for this run
            settings.CACHES['default'].update(cache_params)

            # Clear the cache for a clean test
            cache = caches['default']
            cache.clear()

            # Measure loading time
            start_time = time.time()

            # Cache logic: load products from cache or DB
            cache_key = f"all_products_{cache_timeout}_{max_connections}_{socket_timeout}_{max_entries}"
            products = cache.get(cache_key)
            if not products:
                products = list(Product.objects.all())  # Load products from DB
                cache.set(cache_key, products, timeout=cache_timeout)

            # Simulate data access (fetching from cache)
            _ = cache.get(cache_key)

            elapsed_time = time.time() - start_time
            results[(max_connections, socket_timeout, max_entries, cache_timeout)] = elapsed_time
            self.stdout.write(f"Tested parameters: max_connections={max_connections}, socket_timeout={socket_timeout}, "
                              f"max_entries={max_entries}, timeout={cache_timeout} => Load time: {elapsed_time:.2f}s")

            # Track the best parameters
            if elapsed_time < best_time:
                best_time = elapsed_time
                best_params = (max_connections, socket_timeout, max_entries, cache_timeout)

        # Display the best parameters and load time
        self.stdout.write("\nOptimal Parameters:")
        self.stdout.write(f"max_connections={best_params[0]}, socket_timeout={best_params[1]}, "
                          f"max_entries={best_params[2]}, timeout={best_params[3]} => Load time: {best_time:.2f}s")
