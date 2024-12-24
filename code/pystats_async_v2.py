import asyncio, socket

PYSTATS_VERSION = "1.0"

py_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
py_socket.bind(("127.0.0.1", 28011))
py_socket.setblocking(False)

async def pystats_handler():
    loop = asyncio.get_running_loop()
    queue = asyncio.Queue()  # Create the queue for data storage

    async def listener():
        """Coroutine to receive data and add it to the queue."""
        while True:
            data, _ = await loop.sock_recvfrom(py_socket, 4096)
            data = ' '.join(data.decode('utf-8').split()[2:])
            await queue.put(data if data else "** PyStats has ended **")
            await asyncio.sleep(0.1)

    async def processor():
        """Coroutine to process data from the queue."""
        while True:
            data = await queue.get()  # Get the next item from the queue
            try:
                print(data)  # Process the data
            except Exception as e:
                print(f"Error processing data: {e}")
            queue.task_done()  # Mark the task as done

    # Run listener and processor concurrently
    await asyncio.gather(listener(), processor())

async def main():
    if py_socket:
        print(f"** Started PyStats v{PYSTATS_VERSION} for Starsiege: Tribes **")
    await pystats_handler()

if __name__ == "__main__":
    asyncio.run(main())