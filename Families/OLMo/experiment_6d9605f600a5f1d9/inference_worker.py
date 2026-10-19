
import os, sys, json, time, hashlib, platform, subprocess, shutil
from pathlib import Path
import importlib.metadata
cfg=json.loads(Path(sys.argv[1]).read_text())
os.environ['VLLM_WORKER_MULTIPROC_METHOD']='spawn'
os.environ['TOKENIZERS_PARALLELISM']='false'
os.environ['CUBLAS_WORKSPACE_CONFIG']=':4096:8'
def main():
    import torch
    from vllm import LLM, SamplingParams
    from transformers import AutoTokenizer
    if not torch.cuda.is_available(): raise RuntimeError('Attach a GPU in molab first.')
    prop=torch.cuda.get_device_properties(0)
    # Actual kernel execution catches wheels that omit this GPU's architecture.
    a=torch.ones((64,64), device='cuda'); b=a@a; torch.cuda.synchronize()
    try:
        smi=subprocess.run(['nvidia-smi'],capture_output=True,text=True,timeout=30).stdout
    except (OSError,subprocess.TimeoutExpired): smi='unavailable'
    meta={'gpu':prop.name,'vram':prop.total_memory,'capability':torch.cuda.get_device_capability(),
          'cuda':torch.version.cuda,'torch':torch.__version__, 'python':sys.version,
          'platform':platform.platform(),'cpu_count':os.cpu_count(),'nvidia_smi':smi,
          'disk_free_bytes':shutil.disk_usage(Path(cfg['result']).parent).free,
          'tf32_matmul':torch.backends.cuda.matmul.allow_tf32,
          'deterministic_algorithms':torch.are_deterministic_algorithms_enabled(),
          'packages':{d.metadata['Name']:d.version for d in importlib.metadata.distributions()}}
    Path(cfg['environment']).write_text(json.dumps(meta,indent=2))
    m=cfg['model']
    # Dense BF16 estimate includes a 20% allowance for runtime state, not KV cache.
    # Active MoE parameters do NOT determine storage. Quantized models use explicit/native metadata.
    if not m.get('quantization') and not m.get('native_quantization'):
        estimated=m['size_b']*1e9*2*1.2
        if estimated>prop.total_memory*cfg['gpu_memory_utilization']:
            raise RuntimeError('Estimated weights/runtime exceed GPU budget; choose a documented quantized checkpoint or smaller model.')
    kwargs=dict(model=m['id'],revision=m['revision'],tokenizer_revision=m['revision'],
        dtype=m['dtype'],max_model_len=m['max_model_len'],
        gpu_memory_utilization=cfg['gpu_memory_utilization'],tensor_parallel_size=1,
        trust_remote_code=m['trust_remote_code'],seed=17, enforce_eager=True)
    if m['quantization']: kwargs['quantization']=m['quantization']
    kwargs.update(m.get('engine_kwargs',{}))
    llm=LLM(**kwargs)
    tok=llm.get_tokenizer()
    for start in range(0,len(cfg['jobs']),cfg['batch_size']):
        jobs=cfg['jobs'][start:start+cfg['batch_size']]
        prompts=[]
        for j in jobs:
            if m['kind']=='base': p=j['prompt']
            else:
                if not tok.chat_template: raise ValueError('No native chat template for '+m['id'])
                p=tok.apply_chat_template([{'role':'user','content':j['prompt']}],tokenize=False,
                    add_generation_prompt=True,**m['chat_kwargs'])
            n=len(tok.encode(p,add_special_tokens=False))
            if n+m['max_tokens']>m['max_model_len']:
                raise ValueError('Context overflow: increase max_model_len or decrease generation budget; never silently truncate.')
            j['rendered_prompt']=p
            prompts.append(p)
        params=[SamplingParams(temperature=j['temperature'],top_p=1.0,max_tokens=m['max_tokens'],seed=j['seed']) for j in jobs]
        t=time.perf_counter()
        outputs=llm.generate(prompts,params,use_tqdm=False)
        elapsed=time.perf_counter()-t
        with open(cfg['result'],'a',encoding='utf-8') as f:
            for j,o in zip(jobs,outputs):
                z=o.outputs[0]
                j.update(text=z.text,input_tokens=len(o.prompt_token_ids),output_tokens=len(z.token_ids),
                    finish_reason=z.finish_reason,stop_reason=z.stop_reason,
                    batch_elapsed_s=elapsed,batch_size=len(jobs),batch_start=start,
                    model=m['id'],revision=m['revision'],dtype=m['dtype'],quantization=m['quantization'],
                    utc_completed=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
                f.write(json.dumps(j,ensure_ascii=False)+'\n'); f.flush(); os.fsync(f.fileno())
if __name__=='__main__': main()
