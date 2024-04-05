import time
from zhipuai import ZhipuAI

API_KEY = "a608059a164a09863479fb4d55b4d5d5.TkqSAVJ4F72XE9Pl"


def extend_description(description: str) -> str:
    client = ZhipuAI(api_key=API_KEY)
    myprompt = f'请根据这句古诗“{description}”，给我二到四个现代汉语的短句来描述诗中关键意象，用逗号分割，我要用来绘制一副国画。只用给我几个词就好，不要排序，不要任何解释性的、描述性的话或者注释。'
    response = client.chat.asyncCompletions.create(
        model="glm-4",  # 使用指定的模型
        messages=[
            {
                "role": "user",
                "content": myprompt
            }
        ],
    )

    # 获取任务ID并初始化变量
    task_id = response.id
    task_status = ''
    get_cnt = 0

    # 检查任务状态，直到完成或失败
    while task_status != 'SUCCESS' and task_status != 'FAILED' and get_cnt <= 40:
        result_response = client.chat.asyncCompletions.retrieve_completion_result(id=task_id)
        task_status = result_response.task_status

        # 检查间隔，避免频繁查询
        time.sleep(2)
        get_cnt += 1

    # 任务成功，提取文本
    if task_status == 'SUCCESS':
        expanded_text = result_response.choices[0].message.content
        return expanded_text
    else:
        return description  # 如果任务失败，返回原始描述
