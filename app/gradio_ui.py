import os
import json
import gradio as gr
from app.services.pdf_loader import load_pdf
from app.orchestrator import run_full_review


def format_clause_value(value):
    """Format clause value (dict, list, or string) into human-readable HTML"""
    if value == "not_found" or value is None:
        return "<p style='color: #999; font-style: italic;'>Not found in contract</p>"
    
    if isinstance(value, dict):
        # Format dictionary as a structured list
        html = "<ul style='margin: 0; padding-left: 20px; list-style-type: disc; color: #1a1a1a;'>"
        for k, v in value.items():
            if isinstance(v, list):
                if v:
                    items = ", ".join([str(item).replace('_', ' ').title() for item in v])
                    html += f"<li style='margin-bottom: 8px; color: #1a1a1a;'><strong style='color: #1a1a1a;'>{k.replace('_', ' ').title()}:</strong> <span style='color: #1a1a1a;'>{items}</span></li>"
                else:
                    html += f"<li style='margin-bottom: 8px; color: #1a1a1a;'><strong style='color: #1a1a1a;'>{k.replace('_', ' ').title()}:</strong> <span style='color: #1a1a1a;'>Not specified</span></li>"
            else:
                html += f"<li style='margin-bottom: 8px; color: #1a1a1a;'><strong style='color: #1a1a1a;'>{k.replace('_', ' ').title()}:</strong> <span style='color: #1a1a1a;'>{str(v)}</span></li>"
        html += "</ul>"
        return html
    
    if isinstance(value, list):
        # Format list as bullet points
        if value:
            html = "<ul style='margin: 0; padding-left: 20px; list-style-type: disc; color: #1a1a1a;'>"
            for item in value:
                formatted_item = str(item).replace('_', ' ').title()
                html += f"<li style='margin-bottom: 4px; color: #1a1a1a;'>{formatted_item}</li>"
            html += "</ul>"
            return html
        else:
            return "<p style='color: #999; font-style: italic;'>Not specified</p>"
    
    # Plain string - ensure dark color for visibility
    return f"<p style='margin: 0; color: #1a1a1a; line-height: 1.6;'>{str(value)}</p>"


def analyze_contract(pdf_file, progress=gr.Progress()):
    """Process uploaded PDF and return analysis results"""
    if pdf_file is None:
        return (
            "<p style='text-align: center; color: #666; padding: 40px;'>⚠️ Please upload a PDF file</p>",
            "<p style='text-align: center; color: #666; padding: 40px;'>⚠️ Please upload a PDF file</p>",
            "<p style='text-align: center; color: #666; padding: 40px;'>⚠️ Please upload a PDF file</p>",
            "⚠️ Please upload a PDF file"
        )
    
    try:
        progress(0.1, desc="Loading PDF...")
        
        # Handle file path - Gradio can pass file object or path string
        if isinstance(pdf_file, str):
            file_path = pdf_file
        elif hasattr(pdf_file, 'name'):
            file_path = pdf_file.name
        else:
            raise ValueError("Invalid file object provided")
        
        # Verify file exists before attempting to load
        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}. Please upload the file again.")
        
        # Load PDF
        text = load_pdf(file_path)
        if not text or not text.strip():
            error_msg = "⚠️ PDF appears to be empty or could not be read"
            return (
                f"<p style='text-align: center; color: #c62828; padding: 40px;'>{error_msg}</p>",
                f"<p style='text-align: center; color: #c62828; padding: 40px;'>{error_msg}</p>",
                f"<p style='text-align: center; color: #c62828; padding: 40px;'>{error_msg}</p>",
                error_msg
            )
        
        # Truncate very long content to speed up processing (keep first 8000 chars)
        if len(text) > 8000:
            text = text[:8000] + "\n\n[Content truncated for faster processing...]"
            progress(0.15, desc="Content optimized for processing...")
        
        progress(0.2, desc="Extracting clauses from contract...")
        # Run full review with progress updates
        result = run_full_review(text, progress=progress)
        
        # Format clauses
        clauses_dict = result.get("clauses", {})
        if isinstance(clauses_dict, dict):
            clauses_html = "<div style='max-height: 400px; overflow-y: auto;'>"
            for key, value in clauses_dict.items():
                if key != "error" and key != "raw_response":
                    formatted_value = format_clause_value(value)
                    clauses_html += f"""
                    <div style='margin-bottom: 15px; padding: 12px; background: #f8f9ff; border-radius: 8px; border-left: 4px solid #667eea;'>
                        <h4 style='margin: 0 0 8px 0; color: #667eea; font-weight: 600;'>{key.replace('_', ' ').title()}</h4>
                        <div style='color: #1a1a1a; line-height: 1.6; font-weight: 400;'>{formatted_value}</div>
                    </div>
                    """
            clauses_html += "</div>"
        else:
            clauses_html = f"<p>{str(clauses_dict)}</p>"
        
        # Format risks
        risks_dict = result.get("risks", {})
        if isinstance(risks_dict, dict):
            risks_html = "<div style='max-height: 400px; overflow-y: auto;'>"
            for key, value in risks_dict.items():
                if key != "error" and key != "raw_response":
                    # Determine risk level color
                    risk_str = str(value).lower()
                    if "high" in risk_str or "critical" in risk_str:
                        risk_color = "#c62828"
                        risk_bg = "#ffebee"
                        risk_label = "🔴 HIGH RISK"
                    elif "medium" in risk_str or "moderate" in risk_str:
                        risk_color = "#e65100"
                        risk_bg = "#fff3e0"
                        risk_label = "🟡 MEDIUM RISK"
                    elif "low" in risk_str:
                        risk_color = "#2e7d32"
                        risk_bg = "#e8f5e9"
                        risk_label = "🟢 LOW RISK"
                    else:
                        risk_color = "#666"
                        risk_bg = "#f5f5f5"
                        risk_label = "⚪ UNKNOWN"
                    
                    risks_html += f"""
                    <div style='margin-bottom: 15px; padding: 12px; background: {risk_bg}; border-radius: 8px; border-left: 4px solid {risk_color};'>
                        <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                            <h4 style='margin: 0; color: {risk_color}; font-weight: 600;'>{key.replace('_', ' ').title()}</h4>
                            <span style='margin-left: 10px; padding: 4px 10px; background: {risk_color}; color: white; border-radius: 12px; font-size: 0.75rem; font-weight: 600;'>{risk_label}</span>
                        </div>
                        <p style='margin: 0; color: #1a1a1a; line-height: 1.6; font-weight: 400;'>{str(value)}</p>
                    </div>
                    """
            risks_html += "</div>"
        else:
            risks_html = f"<p>{str(risks_dict)}</p>"
        
        # Format suggestions
        suggestions = result.get("suggestions", "No suggestions available")
        suggestions_html = f"""
        <div style='padding: 20px; background: #fff3cd; border-radius: 8px; border-left: 4px solid #ffc107; max-height: 400px; overflow-y: auto;'>
            <h4 style='margin: 0 0 12px 0; color: #856404; font-weight: 600;'>💡 Revision Suggestions</h4>
            <div style='color: #1a1a1a; line-height: 1.8; white-space: pre-wrap; font-weight: 400;'>{str(suggestions)}</div>
        </div>
        """
        
        # Note: Don't delete the file - Gradio manages temporary files automatically
        # Deleting it causes issues when analyzing the same file multiple times
        
        return clauses_html, risks_html, suggestions_html, "✅ Analysis completed successfully!"
    
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        error_html = f"<p style='text-align: center; color: #c62828; padding: 40px;'>{error_msg}</p>"
        return error_html, error_html, error_html, error_msg


# Create Gradio interface
with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="purple",
        secondary_hue="blue",
        font=("ui-sans-serif", "system-ui", "sans-serif")
    ),
    title="Contract Review & Risk Analysis Agent",
    css="""
    .gradio-container {
        max-width: 1400px !important;
    }
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .main-header p {
        margin: 10px 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    """
) as demo:
    
    gr.HTML("""
    <div class="main-header">
        <h1>📄 Contract Review & Risk Analysis Agent</h1>
        <p>Upload a contract PDF to analyze clauses, identify risks, and get revision suggestions</p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            pdf_input = gr.File(
                label="📎 Upload Contract PDF",
                file_types=[".pdf"],
                type="filepath"
            )
            analyze_btn = gr.Button(
                "🔍 Analyze Contract",
                variant="primary",
                size="lg",
                scale=1
            )
            status = gr.Textbox(
                label="Status",
                interactive=False,
                value="Ready to analyze..."
            )
        
        with gr.Column(scale=2):
            with gr.Tabs():
                with gr.Tab("📋 Extracted Clauses"):
                    clauses_output = gr.HTML(
                        label="Clauses",
                        value="<p style='text-align: center; color: #666; padding: 40px;'>Upload a PDF and click 'Analyze Contract' to see extracted clauses</p>"
                    )
                
                with gr.Tab("⚠️ Risk Analysis"):
                    risks_output = gr.HTML(
                        label="Risks",
                        value="<p style='text-align: center; color: #666; padding: 40px;'>Upload a PDF and click 'Analyze Contract' to see risk analysis</p>"
                    )
                
                with gr.Tab("💡 Revision Suggestions"):
                    suggestions_output = gr.HTML(
                        label="Suggestions",
                        value="<p style='text-align: center; color: #666; padding: 40px;'>Upload a PDF and click 'Analyze Contract' to see revision suggestions</p>"
                    )
    
    # Connect the function to the button
    analyze_btn.click(
        fn=analyze_contract,
        inputs=[pdf_input],
        outputs=[clauses_output, risks_output, suggestions_output, status]
    )
    
    # Also allow Enter key or file upload to trigger analysis
    pdf_input.change(
        fn=lambda x: ("Ready to analyze...") if x else ("Please upload a PDF file"),
        inputs=[pdf_input],
        outputs=[status]
    )


if __name__ == "__main__":
    import os
    import socket
    
    # Get port from environment variable (for Render/cloud deployment) or find free port
    port = os.getenv("PORT")
    if port:
        port = int(port)
        server_name = "0.0.0.0"  # Listen on all interfaces for cloud deployment
    else:
        # Local development: find an available port
        def find_free_port(start_port=7860, max_attempts=10):
            for port in range(start_port, start_port + max_attempts):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.bind(('127.0.0.1', port))
                        return port
                except OSError:
                    continue
            return start_port  # Fallback to default
        
        port = find_free_port()
        server_name = "127.0.0.1"
    
    print(f"🚀 Starting Gradio UI on http://{server_name}:{port}")
    demo.launch(server_name=server_name, server_port=port, share=False)

