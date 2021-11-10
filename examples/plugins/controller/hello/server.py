import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class Plugin(BaseHTTPRequestHandler):

    def args(self):
        return json.loads(self.rfile.read(int(self.headers.get('Content-Length'))))

    def reply(self, reply):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(reply).encode("UTF-8"))

    def unsupported(self):
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        if self.path == '/ParameterSubstitutionPlugin.ParameterPreSubstitution':
            self.reply({'parameters': {'hello': 'good morning'}})
        elif self.path == '/WorkflowLifecycleHook.WorkflowPreOperate':
            self.reply({'workflow': {'metadata': {'annotations': {'hello': 'good morning'}}}})
        elif self.path == '/NodeLifecycleHook.NodePreExecute':
            args = self.args()
            if 'plugin' in args['template'] and 'hello' in args['template']['plugin']:
                self.reply({'node': {'phase': 'Succeeded', 'message': 'Hello workflow!'}})
            else:
                self.reply({})
        else:
            self.unsupported()


if __name__ == '__main__':
    httpd = HTTPServer(('', 4355), Plugin)
    httpd.serve_forever()
