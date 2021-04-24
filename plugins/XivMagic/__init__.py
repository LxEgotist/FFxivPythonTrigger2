from FFxivPythonTrigger import PluginBase, api
from aiohttp import web
from . import DoTextCommand, DoAction, AddressManager


class Magics(object):
    macro_command = DoTextCommand.do_text_command
    do_action = DoAction

    def echo_msg(self, msg):
        DoTextCommand.do_text_command("/e %s" % msg)


class XivMagic(PluginBase):
    name = "XivMagic"

    async def text_command_handler(self, request: web.Request):
        DoTextCommand.do_text_command(await request.text())
        return web.json_response({'msg': 'success'})

    async def use_item_handler(self, request: web.Request):
        try:
            item_id = int(await request.text())
        except ValueError:
            return web.json_response({'msg': 'Value Error'})
        paths = request.path.split('/')
        if len(paths) > 1 and paths[1] == 'hq':
            item_id += 1000000
        DoAction.use_item(item_id)
        return web.json_response({'msg': 'success'})

    def __init__(self):
        super().__init__()
        self.api_class = Magics()
        self.register_api("Magic", self.api_class)
        api.HttpApi.register_post_route('command', self.text_command_handler)
        api.HttpApi.register_post_route('useitem', self.use_item_handler)

    def _start(self):
        self.api_class.echo_msg("magic started")
