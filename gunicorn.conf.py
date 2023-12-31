# gunicorn.conf.py

bind = "0.0.0.0:8000"  # Set the address and port where Gunicorn will bind
workers = 4            # Set the number of worker processes
timeout = 120           # Set the timeout for worker processes
