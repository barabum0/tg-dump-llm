import datetime
import json

from litellm import completion
from pydantic import BaseModel

from models.dump import TelegramDump, TelegramMessage


class ResponseFormat(BaseModel):
    tasks: list[str]


def main() -> None:
    with open("result.json") as file:
        dump_text = file.read()

    dump = TelegramDump.model_validate_json(dump_text)

    print(dump.authors)  # noqa: T201

    my_id = "user6878402662"
    my_messages = filter(lambda m: m.author_id == my_id, dump.messages)
    my_messages_since_june: list[TelegramMessage] = list(
        filter(lambda m: m.date >= datetime.datetime(2025, 6, 1), my_messages)
    )

    print(my_messages_since_june[-1].text)  # noqa: T201

    prompt = """Ты - персональный секретарь, отсматривающий чат планёрки. 
    Ты получишь список сообщений одного конкретного сотрудника. 
    Это могут быть сообщения трёх видов: сообщения о начале работы со списком задач на сегодня, сообщения об окончании работы со списком задач на сегодня и другие сообщения. 
    Твоя задача - выписать все задачи, которые выполнял и выполнил сотрудник. Учти, что одна и та же задача может быть указана в разных сообщениях по-разному. 
    Верни ответ в формате JSON."""
    message_texts = json.dumps([m.text for m in my_messages_since_june], ensure_ascii=False)

    response = completion(
        "openai/o4-mini",
        messages=[
            {"role": "developer", "content": prompt},
            {"role": "user", "content": message_texts},
        ],
        response_format=ResponseFormat,
        max_completion_tokens=50000,
    )

    with open("ai-result.json", "w") as ai_result_file:
        ai_result_file.write(json.dumps(json.loads(response.messages[0].content), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
