from threading import Thread
from .analyzer import ProteinAnalyzer

class Producer(Thread):

    def __init__(self, task_queue, filename):
        Thread.__init__(self)
        self.task_queue = task_queue
        self.filename = filename

    def run(self):
        protan = ProteinAnalyzer(self.filename)
        for seq in protan.parse():
            self.task_queue.put(seq)



class Consumer(Thread):

    def __init__(self, task_queue, result_queue):
        Thread.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        protan = ProteinAnalyzer(None)
        while True:
            seq = self.task_queue.get()
            if seq is None:
                self.task_queue.task_done()
                break

            stats = protan.get_stats(seq)
            self.result_queue.put(stats)
            self.task_queue.task_done()