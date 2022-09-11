from transformers import AutoModelForCausalLM, AutoTokenizer
from logger import LoggingHandler
import torch


class Chat_module(LoggingHandler):
    def __init__(self):
        super().__init__()
        self.log.info(f'Setting up Chat module')
        self.model_name = "microsoft/DialoGPT-medium"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.log.info(f'Tokenizer loaded')
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.log.info(f'Neural network loaded')
        self.chat_history_ids = None
        self.bot_input_ids = None
        self.count = 0
        self.log.info(f'Chat module setup complete')

    def get_response(self, phrase):
        output = None
        input_ids = self.tokenizer.encode(phrase + self.tokenizer.eos_token, return_tensors="pt")
        if self.count == 0:
            self.bot_input_ids = input_ids
            self.count += 1
        else:
            self.bot_input_ids = torch.cat([self.chat_history_ids, input_ids], dim=-1)

        counter = 0
        while output is None or output == '':
            self.chat_history_ids = self.model.generate(
                self.bot_input_ids,
                max_length=1000,
                do_sample=True,
                top_p=0.95,
                top_k=50,
                temperature=0.75,
                pad_token_id=self.tokenizer.eos_token_id
            )

            output = self.tokenizer.decode(
                self.chat_history_ids[:, self.bot_input_ids.shape[-1]:][0],
                skip_special_tokens=True
            )
            self.log.info(f'Generating response attempt {counter}. Output is {output}')
            counter += 1
            if counter > 5:
                output = "Sorry I couldn't understand."
                self.log.warning(f'Limit of attempts reached. Returning "{output}"')
                return output
        self.log.info(f'Alice: {output}')
        return output
