import asyncio, socket

PYSTATS_VERSION = "1.0"

class UDPListener:
    def __init__(self, host, port, batch_size=10):
        self.host = host
        self.port = port
        self.batch_size = batch_size
        self.queue = asyncio.Queue()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.sock.setblocking(False)

    async def socket_reader(self):
        """
        Continuously read data from the socket and put it into the queue.
        """
        loop = asyncio.get_running_loop()
        while True:
            try:
                data = await loop.sock_recv(self.sock, 4096)
                data = ' '.join(data.decode('utf-8').split()[2:])
                await self.queue.put(self.sock)  # Put the socket itself into the queue
                print(data)
            except Exception as e:
                print(f"Error in socket_reader: {e}")
            await asyncio.sleep(0.1)  # Small delay to avoid tight looping

    async def process_data(self, sock):
        """
        Read data directly from the socket and perform processing.
        """
        loop = asyncio.get_running_loop()
        try:
            # Read data from the socket
            data = await loop.sock_recv(sock, 4096)
            processed = await asyncio.to_thread(lambda: ' '.join(data.decode('utf-8').split()[2:]))
            print(processed)
        except Exception as e:
            print(f"Error in process_data: {e}")

    async def queue_listener(self):
        """
        Process sockets from the queue in batches.
        """
        while True:
            # Collect a batch of sockets
            batch = []
            for _ in range(self.batch_size):
                sock = await self.queue.get()
                batch.append(sock)

            # Process each socket in the batch concurrently
            await asyncio.gather(*(self.process_data(sock) for sock in batch))

    async def run(self):
        """
        Start the UDP listener and queue processing tasks.
        """
        print(f"** Started PyStats v{PYSTATS_VERSION} for Starsiege: Tribes **")
        
        reader_task = asyncio.create_task(self.socket_reader())
        listener_task = asyncio.create_task(self.queue_listener())
        await asyncio.gather(reader_task, listener_task)

if __name__ == "__main__":
    listener = UDPListener(host="127.0.0.1", port=28011, batch_size=15)
    asyncio.run(listener.run())