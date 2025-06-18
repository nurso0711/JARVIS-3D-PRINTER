from flask import Flask, jsonify, render_template_string, request
from jarvis_printer.printer.gcode_controller import PrinterController


def create_app() -> Flask:
    """Create the Flask web application."""
    app = Flask(__name__)
    controller = PrinterController()

    INDEX_HTML = """
    <!doctype html>
    <title>JARVIS 3D Printer</title>
    <h1>JARVIS 3D Printer Interface</h1>
    <form id="connect" method="post" action="/connect">
        <button type="submit">Connect</button>
    </form>
    <form id="command" method="post" action="/command">
        <input name="command" placeholder="G-code command"/>
        <button type="submit">Send</button>
    </form>
    <pre id="response"></pre>
    <script>
    document.getElementById('command').onsubmit = async e => {
        e.preventDefault();
        const cmd = e.target.command.value;
        const res = await fetch('/command', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command: cmd})
        });
        const data = await res.json();
        document.getElementById('response').textContent = data.response;
    };
    </script>
    """

    @app.route("/")
    def index():
        """Serve the main interface."""
        return render_template_string(INDEX_HTML)

    @app.route("/connect", methods=["POST"])
    def connect():
        """Connect to the printer."""
        controller.connect()
        return jsonify(status="connected")

    @app.route("/command", methods=["POST"])
    def command():
        """Send a G-code command to the printer."""
        cmd = request.get_json().get("command", "")
        resp = controller.send_command(cmd)
        return jsonify(response=resp)

    @app.route("/disconnect", methods=["POST"])
    def disconnect():
        """Disconnect from the printer."""
        controller.disconnect()
        return jsonify(status="disconnected")

    app.controller = controller
    return app


app = create_app()
