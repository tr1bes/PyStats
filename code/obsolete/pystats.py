import socket, time
from schedule import every, repeat, run_pending

py_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
py_socket.bind(("127.0.0.1", 28011))

@repeat(every(0.1).seconds)
def pystats_listener():
    data, _ = py_socket.recvfrom(4096)
    data = data.decode('utf-8').split()[2::]
    data = ' '.join(data)

    try:
        if data:
        #if ('~w' not in data):
            print(data)
        else:
            print("** PyStats has stopped **")
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    if py_socket:
        print("** Started PyStats v1.0 for Starsiege: Tribes **")

    while True:
        run_pending()
        time.sleep(0.2)
