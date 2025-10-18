#!/usr/bin/env python3
import os
import sys
import readline
from openai import OpenAI
from typing import List, Dict

class DeepSeekChat:
    def __init__(self):
        # 检查API密钥
        self.api_key = os.environ.get('DEEPSEEK_API_KEY')
        if not self.api_key:
            print("错误: 请设置环境变量 DEEPSEEK_API_KEY")
            print("例如: export DEEPSEEK_API_KEY='your-api-key'")
            sys.exit(1)
        
        # 初始化客户端
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )
        
        # 对话历史
        self.messages: List[Dict] = [
            {"role": "system", "content": "你是一个有用的助手，回答要简洁明了。"}
        ]
        
        # 设置readline历史
        self.setup_readline()
        
    def setup_readline(self):
        """设置readline以支持历史记录和更好的编辑体验"""
        # 历史文件路径
        histfile = os.path.join(os.path.expanduser("~"), ".deepseek_chat_history")
        
        try:
            readline.read_history_file(histfile)
        except FileNotFoundError:
            pass
        
        # 设置历史文件大小
        readline.set_history_length(1000)
        
        # 保存历史
        import atexit
        atexit.register(readline.write_history_file, histfile)
        
        # 在支持的环境中启用tab补全
        try:
            readline.parse_and_bind("tab: complete")
        except ImportError:
            pass
    
    def stream_response(self, user_input: str):
        """流式获取并显示响应"""
        # 添加用户消息到历史
        self.messages.append({"role": "user", "content": user_input})
        
        print("\n助手: ", end="", flush=True)
        
        try:
            # 流式调用API
            full_response = ""
            stream = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.messages,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            
            # 添加助手回复到历史
            if full_response:
                self.messages.append({"role": "assistant", "content": full_response})
            
            print("\n")  # 添加空行分隔
            
        except Exception as e:
            print(f"\n错误: 调用API时出现问题 - {str(e)}")
    
    def print_welcome(self):
        """显示欢迎信息"""
        print("=" * 60)
        print("DeepSeek 终端聊天助手")
        print("=" * 60)
        print("功能说明:")
        print("• 输入您的问题开始对话")
        print("• 使用方向键移动光标编辑输入")
        print("• 使用上下箭头查看历史记录")
        print("• 输入 'exit' 或 'quit' 退出程序")
        print("• 输入 'clear' 或 'reset' 清空对话历史")
        print("• 输入 'history' 查看当前对话历史")
        print("=" * 60)
        print()
    
    def clear_history(self):
        """清空对话历史（保留系统提示）"""
        system_msg = self.messages[0]  # 保留系统消息
        self.messages = [system_msg]
        print("对话历史已清空")
    
    def show_history(self):
        """显示当前对话历史"""
        if len(self.messages) <= 1:
            print("当前没有对话历史")
            return
        
        print("\n当前对话历史:")
        print("-" * 40)
        for i, msg in enumerate(self.messages[1:], 1):  # 跳过系统消息
            role = "用户" if msg["role"] == "user" else "助手"
            # 显示前50个字符作为预览
            preview = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
            print(f"{i}. {role}: {preview}")
        print("-" * 40)
    
    def run(self):
        """运行主聊天循环"""
        self.print_welcome()
        
        while True:
            try:
                # 获取用户输入
                user_input = input("您: ").strip()
                
                # 处理特殊命令
                if user_input.lower() in ['exit', 'quit', '退出']:
                    print("再见！")
                    break
                elif user_input.lower() in ['clear', 'reset', '清空']:
                    self.clear_history()
                    continue
                elif user_input.lower() in ['history', '历史']:
                    self.show_history()
                    continue
                elif not user_input:
                    continue  # 忽略空输入
                
                # 处理普通对话
                self.stream_response(user_input)
                
            except KeyboardInterrupt:
                print("\n\n使用 Ctrl+C 退出。输入 'exit' 退出程序。")
            except EOFError:
                print("\n再见！")
                break
            except Exception as e:
                print(f"\n发生错误: {str(e)}")

def main():
    # 检查依赖
    try:
        import readline
    except ImportError:
        print("警告: 该平台可能不支持readline，光标编辑功能可能受限")
    
    try:
        chat = DeepSeekChat()
        chat.run()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {str(e)}")

if __name__ == "__main__":
    main()