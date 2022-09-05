from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class Chat_module:
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-medium"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.chat_history_ids = None
        self.bot_input_ids = None
        self.count = 0

    def get_response(self, phrase):
        output = None
        print(output)
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
            counter += 1
            if counter > 5:
                output = "Sorry I couldn't understand."
                return output
        print(output)
        return output
