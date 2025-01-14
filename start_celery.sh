#!/bin/bash
celery -A myshop worker --loglevel=info --pool=gevent -D
celery -A myshop beat --loglevel=info --detach
sleep infinity
