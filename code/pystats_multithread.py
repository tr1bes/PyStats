import asyncio
import socket
import sys
import time
import winloop

# Re-use of pre-allocated buffers for efficiency and speed
BUFFER_SIZE = 4096
PYSTATS_VERSION = "1.0"

class TribesUDPListener:
    def __init__(self, host, port, max_queue_size=1000, batch_size=10):
        self.host = host
        self.port = port
        self.batch_size = batch_size
        self.queue = asyncio.Queue(maxsize=max_queue_size)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        self.sock.setblocking(False)
        self.start = time.time()
        self.buffer = bytearray(BUFFER_SIZE)
        self.buffer_view = memoryview(self.buffer)
        self.bytes_received = b''

    async def socket_reader(self):
        """
        Continuously read data from the socket and put it into the queue.
        """
        loop = asyncio.get_running_loop()

        while True:
            try:
                self.bytes_received =  await loop.sock_recv_into(self.sock, self.buffer_view)
                if not self.queue.full():
                    await self.queue.put(self.bytes_received)
            except Exception as e:
                print(f"Error in socket_reader: {e}")
            await asyncio.sleep(0.1)  # Small delay to avoid tight looping

    async def batch_processor(self):
        """
        Process sockets from the queue in batches.
        """
        while True:
            batch = []
            for _ in range(self.batch_size):
                try:
                    # Timeout so we do not indefinitely wait for a full batch
                    batch.append(await asyncio.wait_for(self.queue.get(), timeout=0.05))
                except asyncio.TimeoutError:
                    break
            if batch:
                await self.process_batch(batch)

    async def process_batch(self, batch):
        tasks = [
            asyncio.create_task(self.process_message(data)) for data in batch
        ]
        await asyncio.gather(*tasks)

    async def process_message(self, data):
        try:
            message = self.buffer_view[:self.bytes_received]
            message = message.tobytes().decode('utf-8')[12:].strip()
            processed = await asyncio.to_thread(lambda: message)
            print(processed)
        except Exception as e:
            print(f"Error Processing message: {e}")

    async def run(self):
        """
        Start PyStats and queue processing tasks.
        """
        print(f"** Started PyStats v{PYSTATS_VERSION} for Starsiege: Tribes **")
        
        reader_task = asyncio.create_task(self.socket_reader())
        processor_task = asyncio.create_task(self.batch_processor())
        await asyncio.gather(reader_task, processor_task)

if __name__ == "__main__":
    # Faster asyncio loop for Windows
    if sys.platform in ('win32'):
        winloop.install()
    
    listener = TribesUDPListener(host="127.0.0.1", port=28011, batch_size=200)
    asyncio.run(listener.run())