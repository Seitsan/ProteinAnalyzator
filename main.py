import time
from collections import Counter
from queue import Queue
from src.analyzer import ProteinAnalyzer
from pathlib import Path
import click
import csv
import sys
import src.mtclasses
import multiprocessing


def save_data(l, output):
    if output.suffix.lower() == '.csv':
        with open(output, 'w', newline='') as f:
            fields = l[0].keys()
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(l)
    else:
        raise click.BadParameter('Output file format is not ".csv"')


def print_data(l):
    fields = l[0].keys()
    writer = csv.DictWriter(sys.stdout, fieldnames=fields)
    writer.writeheader()
    writer.writerows(l)


def merge_data(analyzer):
    total_list = Counter()
    for seq in analyzer.parse():
        for d in analyzer.get_stats(seq):
            total_list[d['type']] += d['quantity']
    result = [{'type': k, 'quantity': v} for k, v in total_list.items()]
    return result


def process_chunk(chunk):
    local_counter = Counter()
    local_analyzer = ProteinAnalyzer(None)
    for seq in chunk:
        for d in local_analyzer.get_stats(seq):
            local_counter[d['type']] += d['quantity']
    return local_counter


@click.command()
@click.argument("filename", type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path))
@click.option('-o', '--output', type=click.Path(dir_okay=False, writable=True, path_type=Path))
@click.option('-m', '--mode', type=click.Choice(['st', 'mt', 'mp']), default='st',
              help='Working mode: singlethreading, multithreading or multiprocessing')
def main(filename, output, mode):
    if mode == 'st':
        start_time = time.time()
        protan = ProteinAnalyzer(filename)
        result = merge_data(protan)
        if output:
            save_data(result, output)
        else:
            print_data(result)
        end_time = time.time()
        execution_time = end_time - start_time
        click.echo(f'Execution time: {execution_time}')

    elif mode == 'mt':
        start_time = time.time()
        task_queue = Queue()
        result_queue = Queue()
        t1 = src.mtclasses.Producer(task_queue, filename)
        t2 = src.mtclasses.Consumer(task_queue, result_queue)
        t3 = src.mtclasses.Consumer(task_queue, result_queue)
        t4 = src.mtclasses.Consumer(task_queue, result_queue)
        consumers = [t2, t3, t4]
        t1.start()
        for c in consumers:
            c.start()
        t1.join()
        task_queue.join()
        for i in range(3):
            task_queue.put(None)
        for c in consumers:
            c.join()
        total_list = Counter()
        while not result_queue.empty():
            stats_list = result_queue.get()
            for d in stats_list:
                total_list[d['type']] += d['quantity']
        result = [{'type': k, 'quantity': v} for k, v in total_list.items()]
        if output:
            save_data(result, output)
        else:
            print_data(result)
        end_time = time.time()
        execution_time = end_time - start_time
        click.echo(f'Execution time: {execution_time}')

    else:
        start_time = time.time()
        protan = ProteinAnalyzer(filename)
        sequences = list(protan.parse())
        chunks = [sequences[i:i + 1000] for i in range(0, len(sequences), 1000)]
        with multiprocessing.Pool() as pool:
            counters = pool.map(process_chunk, chunks)
        total_counter = Counter()
        for cnt in counters:
            total_counter.update(cnt)
        result = [{'type': k, 'quantity': v} for k, v in total_counter.items()]
        if output:
            save_data(result, output)
        else:
            print_data(result)
        end_time = time.time()
        execution_time = end_time - start_time
        click.echo(f'Execution time: {execution_time}')


if __name__ == '__main__':
    main()