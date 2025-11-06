#!/usr/bin/env python3
"""
Web interface for CryptoLLM using Gradio
"""

import gradio as gr
from crypto_llm import CryptoLLM
from crypto_knowledge import CRYPTO_PROMPTS, get_all_prompts
import os


class CryptoLLMInterface:
    """Gradio interface for CryptoLLM"""

    def __init__(self):
        self.llm = None
        self.conversation_history = []

    def initialize_model(self, model_choice, quantization_bits):
        """Initialize the LLM model"""
        try:
            model_map = {
                "Mistral 7B (Recommended)": "mistral-7b",
                "Phi-2 (Fastest)": "phi-2",
                "TinyLlama (Most Efficient)": "tinyllama",
                "Zephyr 7B": "zephyr-7b",
            }

            model_name = model_map.get(model_choice, "mistral-7b")

            self.llm = CryptoLLM(
                model_name=model_name,
                quantization_bits=int(quantization_bits),
                max_memory_gb=6,
            )

            return "✅ Model loaded successfully!"

        except Exception as e:
            return f"❌ Error loading model: {str(e)}"

    def chat_response(self, message, history, temperature, max_tokens):
        """Generate chat response"""
        if self.llm is None:
            return "Please initialize the model first!"

        try:
            # Convert Gradio history format to our format
            conversation_history = []
            if history:
                for user_msg, assistant_msg in history:
                    if user_msg:
                        conversation_history.append({"role": "user", "content": user_msg})
                    if assistant_msg:
                        conversation_history.append({"role": "assistant", "content": assistant_msg})

            # Generate response
            response = self.llm.generate(
                message,
                conversation_history=conversation_history,
                temperature=temperature,
                max_new_tokens=max_tokens,
            )

            return response

        except Exception as e:
            return f"Error: {str(e)}"

    def quick_question(self, question, temperature, max_tokens):
        """Handle quick questions without chat history"""
        if self.llm is None:
            return "Please initialize the model first!"

        try:
            response = self.llm.generate(
                question,
                temperature=temperature,
                max_new_tokens=max_tokens,
            )
            return response
        except Exception as e:
            return f"Error: {str(e)}"


def create_interface():
    """Create and return the Gradio interface"""
    interface = CryptoLLMInterface()

    # Custom CSS for better styling
    custom_css = """
    .gradio-container {
        font-family: 'Arial', sans-serif;
    }
    .main-header {
        text-align: center;
        color: #00ff99;
        margin-bottom: 20px;
    }
    """

    with gr.Blocks(css=custom_css, title="CryptoLLM") as app:
        gr.Markdown(
            """
            # 🪙 CryptoLLM - Cryptocurrency Expert Assistant

            A specialized AI assistant focused on cryptocurrency knowledge, optimized for 6GB VRAM.

            **Features:**
            - Expert knowledge on Bitcoin, Ethereum, DeFi, NFTs, and more
            - Memory-efficient with 4-bit or 8-bit quantization
            - Multiple model options (Mistral, Phi-2, TinyLlama)
            - Conversational chat interface
            """
        )

        with gr.Tab("💬 Chat"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### Model Settings")

                    model_dropdown = gr.Dropdown(
                        choices=[
                            "Mistral 7B (Recommended)",
                            "Phi-2 (Fastest)",
                            "TinyLlama (Most Efficient)",
                            "Zephyr 7B",
                        ],
                        value="Mistral 7B (Recommended)",
                        label="Select Model",
                    )

                    quantization_radio = gr.Radio(
                        choices=["4", "8"],
                        value="4",
                        label="Quantization (bits)",
                        info="4-bit uses less memory, 8-bit is more accurate",
                    )

                    init_button = gr.Button("Initialize Model", variant="primary")
                    status_text = gr.Textbox(label="Status", interactive=False)

                    gr.Markdown("### Generation Settings")

                    temperature_slider = gr.Slider(
                        minimum=0.1,
                        maximum=1.5,
                        value=0.7,
                        step=0.1,
                        label="Temperature",
                        info="Higher = more creative, Lower = more focused",
                    )

                    max_tokens_slider = gr.Slider(
                        minimum=128,
                        maximum=1024,
                        value=512,
                        step=128,
                        label="Max Tokens",
                        info="Maximum length of response",
                    )

                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(height=500, label="Crypto Expert Chat")
                    msg = gr.Textbox(
                        label="Your Message",
                        placeholder="Ask me anything about cryptocurrency...",
                        lines=2,
                    )
                    with gr.Row():
                        submit_btn = gr.Button("Send", variant="primary")
                        clear_btn = gr.Button("Clear Chat")

            # Example questions
            gr.Markdown("### 📚 Example Questions")
            example_buttons = gr.Examples(
                examples=[
                    ["What is Bitcoin and how does it work?"],
                    ["Explain DeFi and its main use cases"],
                    ["What is the difference between proof-of-work and proof-of-stake?"],
                    ["How do I secure my cryptocurrency?"],
                    ["What are NFTs and why are they valuable?"],
                    ["Explain what a smart contract is"],
                    ["What is yield farming in DeFi?"],
                    ["How does Ethereum's gas system work?"],
                ],
                inputs=msg,
            )

            # Wire up the chat functionality
            init_button.click(
                fn=interface.initialize_model,
                inputs=[model_dropdown, quantization_radio],
                outputs=status_text,
            )

            submit_btn.click(
                fn=interface.chat_response,
                inputs=[msg, chatbot, temperature_slider, max_tokens_slider],
                outputs=chatbot,
            ).then(
                lambda: "",
                None,
                msg,
            )

            msg.submit(
                fn=interface.chat_response,
                inputs=[msg, chatbot, temperature_slider, max_tokens_slider],
                outputs=chatbot,
            ).then(
                lambda: "",
                None,
                msg,
            )

            clear_btn.click(lambda: None, None, chatbot)

        with gr.Tab("❓ Quick Q&A"):
            gr.Markdown("### Ask a quick question without chat history")

            with gr.Row():
                with gr.Column():
                    qa_input = gr.Textbox(
                        label="Your Question",
                        placeholder="What is blockchain?",
                        lines=3,
                    )
                    qa_button = gr.Button("Get Answer", variant="primary")

                    gr.Markdown("### Common Topics")
                    topic_buttons = gr.Radio(
                        choices=list(CRYPTO_PROMPTS.keys()),
                        label="Browse by Topic",
                    )

                with gr.Column():
                    qa_output = gr.Textbox(
                        label="Answer",
                        lines=15,
                        interactive=False,
                    )

            qa_button.click(
                fn=interface.quick_question,
                inputs=[qa_input, temperature_slider, max_tokens_slider],
                outputs=qa_output,
            )

        with gr.Tab("ℹ️ About"):
            gr.Markdown(
                """
                ## About CryptoLLM

                CryptoLLM is a specialized language model focused on cryptocurrency knowledge,
                optimized to run on consumer GPUs with 6GB VRAM.

                ### Supported Models

                - **Mistral 7B**: Best balance of quality and performance (Recommended)
                - **Phi-2**: Smaller 2.7B model, fastest inference
                - **TinyLlama**: Most memory-efficient 1.1B model
                - **Zephyr 7B**: Fine-tuned for helpful, harmless responses

                ### Technical Details

                - **Quantization**: Uses 4-bit or 8-bit quantization via bitsandbytes
                - **Memory Usage**: Optimized for 6GB VRAM using NF4 quantization
                - **Framework**: Built with HuggingFace Transformers and PyTorch

                ### Topics Covered

                - Blockchain technology and consensus mechanisms
                - Bitcoin, Ethereum, and major altcoins
                - DeFi (Decentralized Finance) protocols
                - NFTs and digital assets
                - Cryptocurrency trading and technical analysis
                - Smart contracts and Web3 development
                - Security best practices
                - Tokenomics and crypto economics

                ### Disclaimer

                This AI assistant provides educational information only. Always do your own
                research (DYOR) and never treat this as financial advice. Cryptocurrency
                investments carry significant risk.

                ### Links

                - [GitHub Repository](https://github.com/saikohs257/cannaflux)
                - [Documentation](https://github.com/saikohs257/cannaflux/blob/main/README.md)
                """
            )

    return app


def main():
    """Main entry point"""
    app = create_interface()

    # Get port from environment or use default
    port = int(os.getenv("PORT", 7860))
    host = os.getenv("HOST", "0.0.0.0")

    print("\n" + "="*60)
    print("Starting CryptoLLM Web Interface")
    print("="*60 + "\n")

    app.launch(
        server_name=host,
        server_port=port,
        share=False,
    )


if __name__ == "__main__":
    main()
