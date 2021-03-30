from FFxivPythonTrigger import PluginBase, api
from aiohttp import web
from . import DoTextCommand, DoAction, FrameInject, AddressManager


class Magics(object):
    macro_command = DoTextCommand.do_text_command
    do_action = DoAction

    def __init__(self, ):
        self.frame_hook = FrameInject.FrameInjectHook(AddressManager.frame_inject_addr)

    def unload(self):
        self.frame_hook.uninstall()

    def echo_msg(self, msg):
        DoTextCommand.do_text_command("/e %s" % msg)


class XivMagic(PluginBase):
    name = "XivMagic"

    async def text_command_handler(self, request: web.Request):
        return web.json_response({
            'msg': 'success',
            'rtn': DoTextCommand.do_text_command(
                await request.text()
            )
        })

    def __init__(self):
        super().__init__()
        self.api_class = Magics()
        self.register_api("Magic", self.api_class)
        api.HttpApi.register_post_route('command', self.text_command_handler)

    def _onunload(self):
        self.api_class.unload()

    def _start(self):
        self.api_class.frame_hook.enable()
        self.api_class.echo_msg("magic started")
