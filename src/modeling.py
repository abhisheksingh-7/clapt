from typing import Optional, List, Union, Tuple
import torch as T
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForCausalLM, LlamaForCausalLM
from transformers.modeling_outputs import CausalLMOutputWithPast

MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"


class CLAPT(nn.Module):
    def __init__(self, name_or_path: str) -> None:
        super().__init__()
        self.name_or_path = name_or_path
        self.decoder_with_lm = AutoModelForCausalLM.from_pretrained(name_or_path)
        self.decoder_with_lm.resize_token_embeddings(
            self.decoder_with_lm.config.vocab_size + 1
        )


    def forward(
        self,
        input_ids: T.LongTensor = None,
        attention_mask: Optional[T.Tensor] = None,
        position_ids: Optional[T.LongTensor] = None,
        past_key_values: Optional[List[T.FloatTensor]] = None,
        inputs_embeds: Optional[T.FloatTensor] = None,
        labels: Optional[T.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        cache_position: Optional[T.LongTensor] = None,
    ) -> Union[Tuple, CausalLMOutputWithPast]:
        return self.decoder_with_lm(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            labels=labels,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
            cache_position=cache_position,
        )


def main() -> None:
    device = T.device("cuda:0")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.add_special_tokens(
        {
            "pad_token": "<PAD>",
        }
    )
    model = CLAPT(MODEL_NAME).to(device)
    print(model)
    inputs = tokenizer(
        ["Hello there sir, are you CLAPT?"], return_tensors="pt", padding="longest"
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}
    print(model(**inputs))


if __name__ == "__main__":
    main()