"""Launch script for Gradio UI"""
import os
from app.gradio_ui import demo

if __name__ == "__main__":
    # Use static port 7861 (or from PORT environment variable)
    port = int(os.getenv("PORT", "7861"))
    server_name = "0.0.0.0"
    print(f"🚀 Starting Gradio UI on http://{server_name}:{port}")
    demo.launch(server_name=server_name, server_port=port, share=False)

