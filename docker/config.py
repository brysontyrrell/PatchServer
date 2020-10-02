from multiprocessing import cpu_count

bind = "0.0.0.0:5000"
workers = 2
threads = 2 * cpu_count()
