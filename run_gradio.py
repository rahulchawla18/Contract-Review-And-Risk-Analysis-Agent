"""Launch script for Gradio UI"""
import socket
from app.gradio_ui import demo

def find_free_port(start_port=7860, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return start_port  # Fallback to default

if __name__ == "__main__":
    port = find_free_port()
    print(f"🚀 Starting Gradio UI on http://127.0.0.1:{port}")
    demo.launch(server_name="127.0.0.1", server_port=port, share=False)

