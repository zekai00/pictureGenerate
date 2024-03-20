import time
from zhipuai import ZhipuAI

API_KEY = "a608059a164a09863479fb4d55b4d5d5.TkqSAVJ4F72XE9Pl"


def extend_description(description: str) -> str:
    client = ZhipuAI(api_key=API_KEY)
    myprompt = f'请根据这句古诗“{description}”，创作一个现代汉语描述，这个描述应该能够用来描绘一幅画，这幅画应该展现诗中的意境和情感，就像是将诗中的景象转化成了可视化的艺术作品。五十个字左右。'
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
