processes = []
quantum = 4


class Process:
  def __init__(self, pid, duration, start_time, io_operations):
    self.pid = pid
    self.duration = duration
    self.start_time = start_time
    self.io_operations = io_operations
    self.remaining_time = duration


def print_time(time, queue_processes=[], cpu_processes=[], event=""):
  has_event = event != ""
  has_processes_in_queue = len(queue_processes) > 0
  has_processes_in_cpu = len(cpu_processes) > 0

  print(f"=-=-= TEMPO {time} =-=-=")
  if has_event:
    print(f"#[evento] ${event}")

  if has_processes_in_queue:
    print(f"FILA:", end=" ")
    for process in queue_processes:
      pid = process.pid
      remaining_time = process.remaining_time
      print(f"{pid}({remaining_time})", end=" ")
    print()
  else:
    print("FILA: Não há processos na fila")

  if has_processes_in_cpu:
    print(f"CPU:", end=" ")
    for process in cpu_processes:
      pid = process.pid
      remaining_time = process.remaining_time
      print(f"{pid}({remaining_time})", end=" ")
    print()
  else:
    print("Acabaram os processos!")


def read_file(file_path):
  global processes
  file = open(file_path, "r")
  for line in file:
    process_infos = line.replace("\n", "").split(" ")
    pid = process_infos[0]
    duration = process_infos[1]
    start_time = process_infos[2]
    io_operations = []
    has_io_operations = len(process_infos) > 3

    if has_io_operations:
      io_operations = process_infos[3].split(",")

    process = Process(pid, duration, start_time, io_operations)
    processes.append(process)


def main():
  print("=-=-= Inicio da simulação  =-=-=")
  print("Quantum:", quantum)

  read_file("./input_file.txt")
  #print_time(1, [processes[0]], [processes[1]])
  #print_time(2, [processes[3]], [processes[4]])

  print("=-=-= Término da simulação =-=-=")


if __name__ == "__main__":
  main()
