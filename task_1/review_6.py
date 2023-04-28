class AsyncSharedResourceManager(SomeBasicResourceManager):
    shared_resource = None

    _shared_resource_refcount = 0

    _lock = asyncio.Lock()

    async def __aenter__(self):
        async with self._lock:
            if not self._shared_resource_refcount:
                self.shared_resource = await self._init_resource()
            self._shared_resource_refcount += 1
            return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        async with self._lock:
            self._shared_resource_refcount -= 1
            result = await super().__aexit__(exc_type, exc_val, exc_tb)
            if not self._shared_resource_refcount:
                await self._close_resource()
                self.shared_resource = None
            return result


async def coro():
    async with AsyncSharedResourceManager() as shared_resource_manager:
        await shared_resource_manager.shared_resource.do_smth()


async def main():
    await gather(coro(), coro())