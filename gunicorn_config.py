# import multiprocessing

# bind = "0.0.0.0:8000"
# workers = multiprocessing.cpu_count() * 2 + 1
# worker_class = "gthread"
# threads = 4
# max_requests = 1000
# timeout = 60

command = '/Desktop/Project_DEC_2022/react-django/bin/gunicorn'
pythonpath = 'Desktop/Project_DEC_2022/react-django'
bind = '0.0.0.0:8000'
workers = 3
user = 'admin'
