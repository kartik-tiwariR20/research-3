---
language:
- en
- fr
- es
- pt
tags:
- falcon3
license: other
license_name: falcon-llm-license
license_link: https://falconllm.tii.ae/falcon-terms-and-conditions.html
library_name: transformers
---

<div align="center">
    <img src="https://huggingface.co/datasets/tiiuae/documentation-images/resolve/main/general/falco3-logo.png" alt="drawing" width="500"/>
</div>

# Falcon3-7B-Base

**Falcon3** family of Open Foundation Models is a set of pretrained and instruct LLMs ranging from 1B to 10B.

This repository contains the **Falcon3-7B-Base**. It achieves state of art results (at the time of release) on reasoning, language understanding, instruction following, code and mathematics tasks.
Falcon3-7B-Base supports 4 languages (english, french, spanish, portuguese) and a context length up to 32K.

⚠️ **This is a raw, pretrained model, which should be further finetuned for most usecases.** 

## Model Details
- Architecture
  - transformer based causal decoder only architecture
  - 28 decoder blocks
  - grouped query attention (GQA) for faster inference: 12 query heads and 4 KV heads
  - wider head dimension: 256
  - high RoPE value to support long context understanding: 1000042
  - 32k context length
  - 131k vocab size
- Pretrained on 14 Teratokens of datasets comprising of web, code, STEM, high quality and mutlilingual data using 1024 H100 GPU chips
- Supports EN, FR, ES, PT
- Developed by [Technology Innovation Institute](https://www.tii.ae)
- License: TII Falcon-LLM License 2.0
- Model Release Date: December 2024


## Getting started

<details>
<summary> Click to expand </summary>

```python
import torch
from transformers import pipeline

pipe = pipeline(
    "text-generation", 
    model="tiiuae/Falcon3-7B-Base", 
    torch_dtype=torch.bfloat16, 
    device_map="auto"
)
response = pipe("Question: How many hours in one day? Answer: ")
print(response[0]['generated_text'])
```

</details>

<br>

## Benchmarks
We report in the following table our internal pipeline benchmarks.
 - We use [lm-evaluation harness](https://github.com/EleutherAI/lm-evaluation-harness).
 - We report **raw scores**.
 - We use same batch-size across all models.



<table border="1" style="width: 100%; text-align: center; border-collapse: collapse;">
    <colgroup>
        <col style="width: 10%;">
        <col style="width: 10%;">
        <col style="width: 7%;">
        <col style="width: 7%;">
        <col style="width: 7%;">
        <col style="width: 7%;">
        <col style="background-color: rgba(80, 15, 213, 0.5); width: 7%;">
    </colgroup>
    <thead>
        <tr>
            <th>Category</th>
            <th>Benchmark</th>
            <th>Llama3.1-8B</th>
            <th>Qwen2-7B</th>
            <th>Qwen2.5-7B</th>
            <th>gemma-2-9b</th>
            <th>Falcon3-7B-Base</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="3">General</td>
            <td>MMLU (5-shot)</td>
            <td>65.2</td>
            <td>70.4</td>
            <td>74.2</td>
            <td>-</td>
            <td>67.5</td>
        </tr>
        <tr>
            <td>MMLU-PRO (5-shot)</td>
            <td>32.7</td>
            <td>42.1</td>
            <td>43.5</td>
            <td>-</td>
            <td>39.2</td>
        </tr>
        <tr>
            <td>IFEval</td>
            <td>12.0</td>
            <td>30.6</td>
            <td>33.9</td>
            <td>-</td>
            <td>34.3</td>
        </tr>
        <tr>
            <td rowspan="2">Math</td>
            <td>GSM8K (5-shot)</td>
            <td>49.4</td>
            <td>77.9</td>
            <td>82.9</td>
            <td>-</td>
            <td>76.2</td>
        </tr>
        <tr>
            <td>MATH(4-shot)</td>
            <td>4.1</td>
            <td>17.5</td>
            <td>15.5</td>
            <td>-</td>
            <td>18.0</td>
        </tr>
        <tr>
            <td rowspan="4">Reasoning</td>
            <td>Arc Challenge (25-shot)</td>
            <td>53.4</td>
            <td>57.4</td>
            <td>59.0</td>
            <td>-</td>
            <td>59.6</td>
        </tr>
        <tr>
            <td>GPQA (0-shot)</td>
            <td>31.0</td>
            <td>31.9</td>
            <td>33.0</td>
            <td>-</td>
            <td>35.5</td>
        </tr>
        <tr>
            <td>MUSR (0-shot)</td>
            <td>38.0</td>
            <td>44.1</td>
            <td>44.2</td>
            <td>-</td>
            <td>47.3</td>
        </tr>
        <tr>
            <td>BBH (3-shot)</td>
            <td>46.5</td>
            <td>53.3</td>
            <td>54.0</td>
            <td>-</td>
            <td>51.0</td>
        </tr>
        <tr>
            <td rowspan="4">CommonSense Understanding</td>
            <td>PIQA (0-shot)</td>
            <td>80.3</td>
            <td>79.8</td>
            <td>78.7</td>
            <td>-</td>
            <td>77.7</td>
        </tr>
        <tr>
            <td>SciQ (0-shot)</td>
            <td>96.3</td>
            <td>95.9</td>
            <td>96.6</td>
            <td>-</td>
            <td>95.3</td>
        </tr>
        <tr>
            <td>Winogrande (0-shot)</td>
            <td>74.0</td>
            <td>72.1</td>
            <td>72.9</td>
            <td>-</td>
            <td>71.0</td>
        </tr>
        <tr>
            <td>OpenbookQA (0-shot)</td>
            <td>33.4</td>
            <td>35.2</td>
            <td>33.6</td>
            <td>-</td>
            <td>31.4</td>
        </tr>
    </tbody>
</table>

## Useful links
- View our [release blogpost](https://huggingface.co/blog/falcon3).
- Feel free to join [our discord server](https://discord.gg/fwXpMyGc) if you have any questions or to interact with our researchers and developers.

## Technical Report

Coming soon....

## Citation
If Falcon3 family were helpful to your work, feel free to give us a cite.

```
@misc{Falcon3,
    title = {Falcon 3 family of Open Foundation Models},
    author = {TII Team},
    month = {December},
    year = {2024}
}
```