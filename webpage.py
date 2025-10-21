import gradio as gr
import requests
import json

# API 配置
API_URL = "http://127.0.0.1:8000/chat"


def chat_with_qwen(message, history):
    """与千问API对话"""

    # 转换Gradio历史格式到API格式
    api_history = []
    for human, assistant in history:
        api_history.extend([
            {"role": "user", "content": human},
            {"role": "assistant", "content": assistant}
        ])

    request_data = {
        "prompt": message,
        "history": api_history,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        response = requests.post(
            API_URL,
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=600
        )

        if response.status_code == 200:
            data = response.json()
            return data["response"]
        else:
            return f"❌ API错误: {response.status_code}\n{response.text}"

    except requests.exceptions.ConnectionError:
        return "❌ 无法连接到API服务器，请确保服务正在运行"
    except Exception as e:
        return f"❌ 发生错误: {str(e)}"


# 创建Gradio界面
with gr.Blocks(
        title="千问8B聊天助手",
        theme=gr.themes.Soft()
) as demo:
    gr.Markdown("""
    # 🚀 千问8B智能聊天助手
    基于Qwen1.5-1.8B-Chat大模型的对话系统
    """)

    with gr.Row():
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(
                height=500,
                label="对话记录",
                show_copy_button=True
            )

            with gr.Row():
                msg = gr.Textbox(
                    placeholder="输入您的问题...",
                    lines=2,
                    scale=4,
                    container=False
                )
                send_btn = gr.Button("发送", variant="primary", scale=1)

        with gr.Column(scale=1):
            gr.Markdown("### 参数设置")
            max_tokens = gr.Slider(50, 1024, value=512, label="生成长度")
            temperature = gr.Slider(0.1, 1.0, value=0.7, step=0.1, label="随机性")
            top_p = gr.Slider(0.1, 1.0, value=0.9, step=0.1, label="Top-P")

            clear_btn = gr.Button("清空对话", variant="stop")

            gr.Markdown("### 系统状态")
            status = gr.Textbox(
                value="✅ 点击发送开始对话",
                interactive=False,
                label="状态"
            )


    # 处理用户输入
    def user_message(user_input, chat_history):
        return "", chat_history + [[user_input, None]]


    def bot_message(chat_history, max_tokens_val, temp, top_p_val):
        user_input = chat_history[-1][0]

        # 调用API
        bot_response = chat_with_qwen(user_input, chat_history[:-1])

        chat_history[-1][1] = bot_response
        status_msg = "✅ 回复完成" if not bot_response.startswith("❌") else "❌ 发生错误"

        return chat_history, status_msg


    # 绑定事件
    submit_event = msg.submit(
        user_message,
        [msg, chatbot],
        [msg, chatbot]
    ).then(
        bot_message,
        [chatbot, max_tokens, temperature, top_p],
        [chatbot, status]
    )

    send_click = send_btn.click(
        user_message,
        [msg, chatbot],
        [msg, chatbot]
    ).then(
        bot_message,
        [chatbot, max_tokens, temperature, top_p],
        [chatbot, status]
    )

    clear_btn.click(
        lambda: ([], "✅ 对话已清空"),
        outputs=[chatbot, status]
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )