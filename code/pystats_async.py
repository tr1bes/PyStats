import asyncio, socket

PYSTATS_VERSION = "1.0"

py_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
py_socket.bind(("127.0.0.1", 28011))
py_socket.setblocking(False)

async def pystats_listener():
    loop = asyncio.get_running_loop()
    while True:
        data, _ = await loop.sock_recvfrom(py_socket, 4096)
        data = data.decode('utf-8').split()[2:]
        data = ' '.join(data)

        try:
            if data:
                print(data)
            else:
                print("** PyStats has stopped **")
        except Exception as e:
            print(f"Error: {e}")
        await asyncio.sleep(0.1)

async def main():
    if py_socket:
        print(f"** Started PyStats v{PYSTATS_VERSION} for Starsiege: Tribes **")
    await pystats_listener()

if __name__ == "__main__":
    asyncio.run(main())
