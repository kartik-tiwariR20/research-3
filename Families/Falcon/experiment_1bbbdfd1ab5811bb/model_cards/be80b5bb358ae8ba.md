---
base_model: tiiuae/Falcon3-10B-Base
library_name: transformers
license: other
license_name: falcon-llm-license
license_link: https://falconllm.tii.ae/falcon-terms-and-conditions.html
tags:
- falcon3
model-index:
- name: Falcon3-10B-Instruct
  results:
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: IFEval (0-Shot)
      type: HuggingFaceH4/ifeval
      args:
        num_few_shot: 0
    metrics:
    - type: inst_level_strict_acc and prompt_level_strict_acc
      value: 78.17
      name: strict accuracy
    source:
      url: https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard?query=tiiuae/Falcon3-10B-Instruct
      name: Open LLM Leaderboard
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: BBH (3-Shot)
      type: BBH
      args:
        num_few_shot: 3
    metrics:
    - type: acc_norm
      value: 44.82
      name: normalized accuracy
    source:
      url: https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard?query=tiiuae/Falcon3-10B-Instruct
      name: Open LLM Leaderboard
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: MATH Lvl 5 (4-Shot)
      type: hendrycks/competition_math
      args:
        num_few_shot: 4
    metrics:
    - type: exact_match
      value: 25.91
      name: exact match
    source:
      url: https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard?query=tiiuae/Falcon3-10B-Instruct
      name: Open LLM Leaderboard
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: GPQA (0-shot)
      type: Idavidrein/gpqa
      args:
        num_few_shot: 0
    metrics:
    - type: acc_norm
      value: 10.51
      name: acc_norm
    source:
      url: https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard?query=tiiuae/Falcon3-10B-Instruct
      name: Open LLM Leaderboard
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: MuSR (0-shot)
      type: TAUR-Lab/MuSR
      args:
        num_few_shot: 0
    metrics:
    - type: acc_norm
      value: 13.61
      name: acc_norm
    source:
      url: https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard?query=tiiuae/Falcon3-10B-Instruct
      name: Open LLM Leaderboard
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: MMLU-PRO (5-shot)
      type: TIGER-Lab/MMLU-Pro
      config: main
      split: test
      args:
        num_few_shot: 5
    metrics:
    - type: acc
      value: 38.1
      name: accuracy
    source:
      url: https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard?query=tiiuae/Falcon3-10B-Instruct
      name: Open LLM Leaderboard
---

<div align="center">
    <img src="https://huggingface.co/datasets/tiiuae/documentation-images/resolve/main/general/falco3-logo.png" alt="drawing" width="500"/>
</div>

# Falcon3-10B-Instruct

**Falcon3** family of Open Foundation Models is a set of pretrained and instruct LLMs ranging from 1B to 10B parameters.

This repository contains the **Falcon3-10B-Instruct**. It achieves state-of-the-art results (at the time of release) on reasoning, language understanding, instruction following, code and mathematics tasks.
Falcon3-10B-Instruct supports 4 languages (English, French, Spanish, Portuguese) and a context length of up to 32K.


## Model Details
- Architecture
  - Transformer-based causal decoder-only architecture
  - 40 decoder blocks
  - Grouped Query Attention (GQA) for faster inference: 12 query heads and 4 key-value heads
  - Wider head dimension: 256
  - High RoPE value to support long context understanding: 1000042
  - Uses SwiGLu and RMSNorm
  - 32K context length
  - 131K vocab size
- Depth up-scaled from **Falcon3-7B-Base** with 2 Teratokens of datasets comprising of web, code, STEM, high quality and mutlilingual data using 1024 H100 GPU chips
- Posttrained on 1.2 million samples of STEM, conversational, code, safety and function call data
- Supports EN, FR, ES, PT
- Developed by [Technology Innovation Institute](https://www.tii.ae)
- License: TII Falcon-LLM License 2.0
- Model Release Date: December 2024


## Getting started

<details>
<summary> Click to expand </summary>

```python
from transformers import AutoTokenizer, AutoModelForCausalLM


from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "tiiuae/Falcon3-10B-Instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "How many hours in one day?"
messages = [
    {"role": "system", "content": "You are a helpful friendly assistant Falcon3 from TII, try to follow instructions as much as possible."},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=1024
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(response)
```

</details>

<br>

## Benchmarks
We report the official HuggingFace leaderboard normalized evaluations [Open LLM Leaderboard Evaluation Results](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) in the following table.
<table border="1" style="width: 100%; text-align: center; border-collapse: collapse;">
    <colgroup>
        <col style="width: 10%;">
        <col style="width: 7%;">
        <col style="width: 7%;">
        <col style="width: 7%;">
        <col style="background-color: rgba(80, 15, 213, 0.5); width: 7%;">
    </colgroup>
    <thead>
        <tr>
            <th>Benchmark</th>
            <th>Yi-1.5-9B-Chat</th>
            <th>Mistral-Nemo-Instruct-2407 (12B)</th>
            <th>Gemma-2-9b-it</th>
            <th>Falcon3-10B-Instruct</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>IFEval</td>
            <td>60.46</td>
            <td>63.80</td>
            <td>74.36</td>
            <td><b>78.17</b></td>
        </tr>
        <tr>
            <td>BBH (3-shot)</td>
            <td>36.95</td>
            <td>29.68</td>
            <td>42.14</td>
            <td><b>44.82</b></td>
        </tr>
        <tr>
            <td>MATH Lvl-5 (4-shot)</td>
            <td>12.76</td>
            <td>6.50</td>
            <td>0.23</td>
            <td><b>25.91</b></td>
        </tr>              
        <tr>
            <td>GPQA (0-shot)</td>
            <td>11.30</td>
            <td>5.37</td>
            <td><b>14.77</b></td>
            <td>10.51</td>
        </tr>
        <tr>
            <td>MUSR (0-shot)</td>
            <td>12.84</td>
            <td>8.48</td>
            <td>9.74</td>
            <td><b>13.61</b></td>
        </tr>
        <tr>
            <td>MMLU-PRO (5-shot)</td>
            <td>33.06</td>
            <td>27.97</td>
            <td>31.95</td>
            <td><b>38.10</b></td>
        </tr>        
    </tbody>
</table>

Also, we report in the following table our internal pipeline benchmarks.
 - We use [lm-evaluation harness](https://github.com/EleutherAI/lm-evaluation-harness).
 - We report **raw scores** obtained by applying chat template and fewshot_as_multiturn.
 - We use same batch-size across all models.

<table border="1" style="width: 100%; text-align: center; border-collapse: collapse;">
    <colgroup>
        <col style="width: 10%;">
        <col style="width: 10%;">
        <col style="width: 7%;">
        <col style="width: 7%;">
        <col style="background-color: rgba(80, 15, 213, 0.5); width: 7%;">
    </colgroup>
    <thead>
        <tr>
            <th>Category</th>
            <th>Benchmark</th>       
            <th>Yi-1.5-9B-Chat</th>
            <th>Mistral-Nemo-Instruct-2407 (12B)</th>
            <th>Falcon3-10B-Instruct</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="3">General</td>
            <td>MMLU (5-shot)</td>
            <td>68.8</td>
            <td>66.0</td>
            <td><b>73.9</b></td>
        </tr>
        <tr>
            <td>MMLU-PRO (5-shot)</td>
            <td>38.8</td>
            <td>34.3</td>
            <td><b>44</b></td>
        </tr>
        <tr>
            <td>IFEval</td>
            <td>57.8</td>
            <td>63.4</td>
            <td><b>78</b></td>
        </tr>
        <tr>
            <td rowspan="3">Math</td>
            <td>GSM8K (5-shot)</td>
            <td>77.1</td>
            <td>77.6</td>
            <td><b>84.9</b></td>
        </tr>
        <tr>
            <td>GSM8K (8-shot, COT)</td>
            <td>76</td>
            <td>80.4</td>
            <td><b>84.6</b></td>
        </tr>
        <tr>
            <td>MATH Lvl-5 (4-shot)</td>
            <td>3.3</td>
            <td>5.9</td>
            <td><b>22.1</b></td>
        </tr>
        <tr>
            <td rowspan="5">Reasoning</td>
            <td>Arc Challenge (25-shot)</td>
            <td>58.3</td>
            <td>63.4</td>
            <td><b>66.2</b></td>
        </tr>
        <tr>
            <td>GPQA (0-shot)</td>
            <td><b>35.6</b></td>
            <td>33.2</td>
            <td>33.5</td>
        </tr>
        <tr>
            <td>GPQA (0-shot, COT)</td>
            <td>16</td>
            <td>12.7</td>
            <td><b>32.6</b></td>
        </tr>
        <tr>
            <td>MUSR (0-shot)</td>
            <td><b>41.9</b></td>
            <td>38.1</td>
            <td>41.1</td>
        </tr>
        <tr>
            <td>BBH (3-shot)</td>
            <td>50.6</td>
            <td>47.5</td>
            <td><b>58.4</b></td>
        </tr>
        <tr>
            <td rowspan="4">CommonSense Understanding</td>
            <td>PIQA (0-shot)</td>
            <td>76.4</td>
            <td>78.2</td>
            <td><b>78.4</b></td>
        </tr>
        <tr>
            <td>SciQ (0-shot)</td>
            <td>61.7</td>
            <td>76.4</td>
            <td><b>90.4</b></td>
        </tr>
        <tr>
            <td>Winogrande (0-shot)</td>
            <td>-</td>
            <td>-</td>
            <td>71</td>
        </tr>
        <tr>
            <td>OpenbookQA (0-shot)</td>
            <td>43.2</td>
            <td>47.4</td>
            <td><b>48.2</b></td>
        </tr>
        <tr>
            <td rowspan="2">Instructions following</td>
            <td>MT-Bench (avg)</td>
            <td>8.3</td>
            <td><b>8.6</b></td>
            <td>8.2</td>
        </tr>
        <tr>
            <td>Alpaca (WC)</td>
            <td>25.8</td>
            <td><b>45.4</b></td>
            <td>24.7</td>
        </tr>
        <tr>
            <td>Tool use</td>
            <td>BFCL AST (avg)</td>
            <td>48.4</td>
            <td>74.2</td>
            <td><b>90.5</b></td>
        </tr>
        <tr>
            <td rowspan="2">Code</td>
            <td>EvalPlus (0-shot) (avg)</td>
            <td>69.4</td>
            <td>58.9</td>
            <td><b>74.7</b></td>
        </tr>
        <tr>
            <td>Multipl-E (0-shot) (avg)</td>
            <td>-</td>
            <td>34.5</td>
            <td><b>45.8</b></td>
        </tr>      
    </tbody>
</table>

## Useful links
- View our [release blogpost](https://huggingface.co/blog/falcon3).
- Feel free to join [our discord server](https://discord.gg/fwXpMyGc) if you have any questions or to interact with our researchers and developers.
  
## Technical Report

Coming soon....

## Citation
If Falcon3 family were helpful in your work, feel free to give us a cite.

```
@misc{Falcon3,
    title = {The Falcon 3 family of Open Models},
    author = {TII Team},
    month = {December},
    year = {2024}
}
```


# [Open LLM Leaderboard Evaluation Results](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)
Detailed results can be found [here](https://huggingface.co/datasets/open-llm-leaderboard/tiiuae__Falcon3-10B-Instruct-details)

|      Metric       |Value|
|-------------------|----:|
|Avg.               |35.19|
|IFEval (0-Shot)    |78.17|
|BBH (3-Shot)       |44.82|
|MATH Lvl 5 (4-Shot)|25.91|
|GPQA (0-shot)      |10.51|
|MuSR (0-shot)      |13.61|
|MMLU-PRO (5-shot)  |38.10|

