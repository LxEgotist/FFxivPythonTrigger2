from FFxivPythonTrigger import PluginBase, api
from aiohttp import web
from . import DoTextCommand, DoAction


class Magics(object):
    macro_command = DoTextCommand.do_text_command
    do_action = DoAction

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

    def _start(self):
        self.api_class.echo_msg("magic started")
