import serial
import threading
from datetime import datetime
import queue

ser_port = 'COM1'
baud_rate = 9600

def get_lap_time(old_time, new_time):
    time_diff = new_time - old_time
    minutes, seconds = divmod(time_diff.seconds, 60)
    microseconds = time_diff.microseconds
    return f"{minutes:02}:{seconds:02}.{microseconds // 10000:02}"

def monitor_trigger(serial_queue):
    # while True:
    #     input_date = input()
    #     current_time = datetime.now()
    #     serial_queue.put(current_time)
    with serial.Serial(ser_port, baud_rate) as ser:
        while True:
            input_data = ser.readline().decode().strip()
            current_time = datetime.now()
            serial_queue.put(current_time)

serial_queue = queue.Queue()
serial_thread = threading.Thread(target=monitor_trigger, args=(serial_queue,), daemon=True)

def main():
    serial_thread.start()
    current_lap = 0
    old_time = None
    init_time = None

    try:
        while True:
            if not serial_queue.empty():
                new_time = serial_queue.get()

                if old_time:
                    current_lap += 1
                    lap_time = get_lap_time(old_time, new_time)
                    with open(log_file, 'a') as logfile:
                        print(f"Lap {current_lap}: {lap_time}", file=logfile)
                    
                old_time = new_time
                if not init_time:
                    init_time = old_time
    except KeyboardInterrupt:
        if init_time:
            with open(log_file, 'a') as logfile:
                print(f"{current_lap} Lap Time: {get_lap_time(init_time, new_time)}", file=logfile)
        serial_thread.join()



if __name__ == '__main__':
    log_file = 'time.log'
    main()
