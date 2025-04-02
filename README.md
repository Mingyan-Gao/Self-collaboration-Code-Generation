# Self-collaboration Code Generation via ChatGPT
[**Paper**](https://arxiv.org/abs/2304.07590) (Accepted to TOSEM)

## Run code
```bash
# generate
bash run.sh
# evaluate
bash evaluate.sh
```

## Add DS-1000
ds1000_gemini.py run generation framework on DS-1000
ds1000_direct_gemini.py directly call gemini 
results folder has the result error rate and logging result reason (empty fail reason mean assertion error)
data has the original ds-1000 dataset and the generated answer
 
## Citation
```
@article{dong2023self,
  title={Self-collaboration code generation via chatgpt},
  author={Dong, Yihong and Jiang, Xue and Jin, Zhi and Li, Ge},
  journal={arXiv preprint arXiv:2304.07590},
  year={2023}
}
```


