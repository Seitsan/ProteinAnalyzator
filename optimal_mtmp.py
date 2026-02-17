import time
from queue import Queue
import src
from collections import Counter
from ProteinAnalyzator.main import print_data, process_chunk
import pandas as pd
from ProteinAnalyzator.src.analyzer import ProteinAnalyzer
import multiprocessing

all_benchmarks = []

# For multithreading
filename = "data/insulin.fasta"
for i in range(1, 11):
    print(f"{i} threads")
    start_time = time.time()
    task_queue = Queue()
    result_queue = Queue()
    t1 = src.mtclasses.Producer(task_queue, filename)
    consumers = [src.mtclasses.Consumer(task_queue, result_queue) for _ in range(i)]
    t1.start()
    for c in consumers:
        c.start()
    t1.join()
    task_queue.join()
    for _ in range(i):
        task_queue.put(None)
    for c in consumers:
        c.join()
    total_list = Counter()
    while not result_queue.empty():
        stats_list = result_queue.get()
        for d in stats_list:
            total_list[d['type']] += d['quantity']
    result = [{'type': k, 'quantity': v} for k, v in total_list.items()]
    print_data(result)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f'Execution time: {execution_time}')

    all_benchmarks.append({
        'type': 'multithreading',
        'num_workers': i,
        'time': execution_time
    })

# For multiprocessing
# if __name__ == '__main__':
#     filename = "data/insulin.fasta"
#     all_benchmarks = []
#     protan = ProteinAnalyzer(filename)
#     sequences = list(protan.parse())
#     chunks = [sequences[i:i + 1000] for i in range(0, len(sequences), 1000)]
#
#     for processes in range(1, 11):
#         start_time = time.time()
#         with multiprocessing.Pool(processes=processes) as pool:
#             counters = pool.map(process_chunk, chunks)
#         total_counter = Counter()
#         for cnt in counters:
#             total_counter.update(cnt)
#         result = [{'type': k, 'quantity': v} for k, v in total_counter.items()]
#         print_data(result)
#         end_time = time.time()
#         execution_time = end_time - start_time
#         print(execution_time)
#
#         all_benchmarks.append({
#             'type': 'multiprocessing',
#             'num_workers': processes,
#             'time': execution_time
#         })
#
#     df_results = pd.DataFrame(all_benchmarks)
#     print(df_results)
