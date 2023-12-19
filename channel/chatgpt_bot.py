
import openai

class ChatGPTBot:
    def __init__(self):
        openai.api_key = 'pk-fDccOgTqDelF8Ydy95QmScdr1o9wtKE7NJNZ-OFa1sY'
        openai.api_base = 'https://pandora.ai-note.xyz/goodluck_711/v1'
        self.args = {
            "model": "gpt-3.5-turbo",  # 对话模型的名称
            "temperature":  0.9,  # 值在[0,1]之间，越大表示回复越具有不确定性
            # "max_tokens":4096,  # 回复最大的字符数
            "top_p":  1,
            "frequency_penalty":  0.0,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
            "presence_penalty": 0.0,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
            "request_timeout": None,  # 请求超时时间，openai接口默认设置为600，对于难问题一般需要较长时间
            "timeout":  None,  # 重试超时时间，在这个时间内，将会自动重试
        }

    def chatgpt(self,prompt,message):

        content = f"我希望你按照这个{prompt},对{message}进行处理,按要求回复"
        messages = [{"role": "user", "content": content}]
        args = self.args
        completion = openai.ChatCompletion.create(
            messages=messages,**args
        )

        chat_response = completion
        answer = chat_response.choices[0].message.content

        return answer


if __name__=='__main__':
    prompt='帮我总结如下这段内容，请简要回复，不超过50个字'
    message='【大商所、郑商所夜盘收盘 PX涨超1%】大商所、郑商所夜盘收盘，涨多跌少。棕榈油、PX等涨超1%，菜粕、纯碱等小幅上涨；玉米跌超1%，玻璃、焦煤等小幅下跌。上期所LU燃油涨超3%。'
    summary=ChatGPTBot().chatgpt(prompt=prompt,message=message)
    print(summary)