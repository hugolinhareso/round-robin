import operator
import pandas as pd
import plotly.figure_factory as ff


processes = []
gantt_data = []
quantum = 4
total_time = 0


class Process:
  def __init__(self, pid, duration, arrival_time, io_operations):
    self.pid = pid
    self.duration = duration
    self.remaining_time = duration
    self.arrival_time = arrival_time
    self.waiting_time = 0
    self.io_operations = io_operations


def append_to_gantt_data(pid, start_time, end_time):
  gantt_data.append(
    dict(Task=pid, Start=start_time, Finish=end_time)
  )


def show_gantt_chart():
  data_frame = pd.DataFrame(gantt_data)
  figure = ff.create_gantt(data_frame, bar_width = 0.4, show_colorbar=True, title="Processo na CPU x Tempo", index_col="Task")
  figure.update_layout(xaxis_type="linear", autosize=False)
  figure.update_yaxes(autorange="reversed")
  figure.show()


def round_robin():
  queue_processes = []
  cpu_processes = []
  current_quantum = 0
  start_time = 0
  end_time = 0
  for time in range(total_time + 1):
    if time == 0:
      cpu_processes.append(processes[0])
      print_time(time, queue_processes, cpu_processes, "")
    else:
      incoming_processes = list(filter(lambda p: p.arrival_time == time, processes))
      current_process = cpu_processes[0]
      events = []

      if (current_process.remaining_time - 1) > 0:
        current_process.remaining_time -= 1
        current_quantum += 1
      elif len(queue_processes) > 0:
        end_time = time
        append_to_gantt_data(current_process.pid, start_time, end_time)
        cpu_processes = [queue_processes[0]]
        start_time = time
        queue_processes.pop(0)
        current_quantum = 0
        events.append(f"ENCERRANDO <{current_process.pid}>")
        update_waiting_time(queue_processes)
        print_time(time, queue_processes, cpu_processes, events)
        continue

      if (current_process.duration - current_process.remaining_time) in current_process.io_operations and len(queue_processes) > 0:
        end_time = time
        append_to_gantt_data(current_process.pid, start_time, end_time)
        cpu_processes = [queue_processes[0]]
        start_time = time
        queue_processes.pop(0)
        queue_processes.append(current_process)
        events.append(f"OPERAÇÃO I/O <{current_process.pid}>")
        current_quantum = 0

      if len(incoming_processes) > 0:
        incoming_process = incoming_processes[0]
        queue_processes.append(incoming_process)
        events.append(f"CHEGADA <{incoming_process.pid}>")

      if current_quantum >= quantum and len(queue_processes) > 0:
        current_process = cpu_processes[0]
        end_time = time
        append_to_gantt_data(current_process.pid, start_time, end_time)
        cpu_processes = [queue_processes[0]]
        start_time = time
        queue_processes.pop(0)
        queue_processes.append(current_process)
        events.append(f"FIM QUANTUM <{current_process.pid}>")
        current_quantum = 0
      
      if time == total_time:
        end_time = time
        append_to_gantt_data(current_process.pid, start_time, end_time)
        cpu_processes = []

      update_waiting_time(queue_processes)
      print_time(time, queue_processes, cpu_processes, events)


def print_time(time, queue_processes=[], cpu_processes=[], events=[]):
  has_events = len(events) > 0
  has_processes_in_queue = len(queue_processes) > 0
  has_processes_in_cpu = len(cpu_processes) > 0

  print(f"=-=-= TEMPO {time} =-=-=")
  if has_events:
    for event in events:
      print(f"#[evento] {event}")

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


def update_waiting_time(queue_processes):
  for process in queue_processes:
    process.waiting_time += 1


def print_waiting_time():
  global processes
  processes.sort(key=operator.attrgetter("pid"))
  print("Tempos de espera:")
  average_waiting_time = 0
  for process in processes:
    print(f"{process.pid}: {process.waiting_time}")
    average_waiting_time += process.waiting_time
  average_waiting_time /= len(processes)
  print(f"Tempo de espera médio: {average_waiting_time}")


def read_file(file_path):
  global processes, total_time
  file = open(file_path, "r")
  for line in file:
    process_infos = line.replace("\n", "").split(" ")
    pid = process_infos[0]
    duration = process_infos[1]
    arrival_time = process_infos[2]
    io_operations = []
    has_io_operations = len(process_infos) > 3

    if has_io_operations:
      for time in process_infos[3].split(","):
        io_operations.append(int(time))

    process = Process(pid, int(duration), int(arrival_time), io_operations)
    total_time += process.duration
    processes.append(process)
  processes.sort(key=operator.attrgetter("arrival_time"))


def main():
  print("=-=-= Inicio da simulação  =-=-=")
  print("Quantum:", quantum)

  read_file("./input_file.txt")
  round_robin()

  print("=-=-= Término da simulação =-=-=")

  print_waiting_time()
  show_gantt_chart()


if __name__ == "__main__":
  main()
