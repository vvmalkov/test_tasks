class AsyncSharedResourceManager(SomeBasicResourceManager):
    _shared_resource = None

    _shared_resource_refcount = 0

    def __aenter__(self):

        if not self._shared_resource_refcount:
            self._shared_resource = await self._init_resource()

        self._shared_resource_refcount += 1

    def __aexit__(self, exc_type, exc_val, exc_tb):

        self._shared_resource_refcount -= 1

        if not self._shared_resource_refcount:
            self._shared_resource = await self._close_resource()


async def coro():
    async with AsyncSharedResourceManager() as shared_resource_manager:
        await shared_resource_manager.shared_resource.do_smth()


async def main():
    await gather(coro(), coro())