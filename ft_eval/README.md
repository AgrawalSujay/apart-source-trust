# Fine-tune evaluation on Kaggle

## 1. Upload the private dataset

1. On the Mac, open Terminal in the repository and run `python3 ft_eval/prepare.py` if you need to rebuild the provided ZIP. It uses local checkpoints only. The ZIP and package directory are generated artifacts.
2. Sign in to Kaggle. Open **Datasets**, choose **New Dataset**, and upload `ft_eval/ft_eval_package.zip`. Name it **apart-ft-eval** and keep visibility **Private**. Click **Create** and wait for the dataset to finish processing.
3. Check the dataset’s file list. The package root should contain `eval.py`, `episodes.jsonl`, `manifest.json` and `adapters/`. If Kaggle kept the ZIP as one file, extract it in the notebook using the cell below. The archive is sized against a conservative 100 GB threshold. Each adapter is about 162 MiB before compression. Allow space for the uploaded dataset within your remaining account quota.

## 2. Start the notebook

1. Open **Code** and click **New Notebook**.
2. In the right sidebar, choose **Add Input** or **Add Data**, open **Your Work** or **Datasets**, search for **apart-ft-eval**, and add it.
3. In **Settings** or **Session options**, set **Accelerator** to **GPU T4 ×2** or **GPU P100**, then switch **Internet** on. Run `!nvidia-smi` in a code cell to confirm the device. If settings are unavailable, check Kaggle’s account verification and accelerator quota.
4. Find the actual attached path in the sidebar or by running `!find /kaggle/input -name eval.py -o -name ft_eval_package.zip`. Use that path in a new code cell:

   ```python
   !python /kaggle/input/<dataset>/eval.py
   ```

   If the input contains only the ZIP, substitute its full path:

   ```python
   !unzip -q /kaggle/input/<dataset>/ft_eval_package.zip -d /kaggle/working/ft_package
   !python /kaggle/working/ft_package/eval.py
   ```

The script installs its dependencies, then uses the checkpoint-named base if its weights are available. Otherwise it uses the public Qwen base for all three arms and prints that choice. It checks every LoRA target against the loaded multimodal architecture. Generation uses text only, the shared checkpoint template, and greedy decoding with thinking disabled. Each fp16 arm uses one GPU, with a default batch size of 8. If memory is tight, rerun with `--batch-size 4` or `--batch-size 2`. A first batch with non-finite scores triggers an fp32 retry for the entire arm at batch size 1. That fallback can use both GPUs and CPU memory.

If a P100 session reports that its PyTorch build cannot run on the GPU, switch to T4 or first install a Pascal-compatible build in that notebook:

```python
!python -m pip install torch==2.7.1 torchvision==0.22.1 torchaudio==2.7.1 --index-url https://download.pytorch.org/whl/cu118
```

For planning, allow **roughly 30–140 minutes per fp16 arm**, plus package installation and the initial base download. This is an estimate assuming roughly 150–250 generated tokens per example and 35–100 aggregate generated tokens per second. The first batch prints a measured estimate. A P100, long replies, or fp32 CPU offload can take longer. Run individual arms with `--arms qwen3.5-4b-base`, `--arms qwen3.5-4b-ft-en`, or `--arms qwen3.5-4b-ft-multi` if you need to split the work across sessions.

## 3. Download and analyse

1. In the notebook sidebar, open **Files** and expand **Output** or **/kaggle/working**. Refresh the file list after generation.
2. Use the menu beside each file to download `qwen3.5-4b-base.jsonl`, `qwen3.5-4b-ft-en.jsonl`, and `qwen3.5-4b-ft-multi.jsonl`. Each completed file has 1,152 rows. You can also use **Save Version** and download from that version’s **Output** tab.
3. If saving a partial run for a fresh session, download each in-progress JSONL **and** its matching `.meta.json`. Restore both to `/kaggle/working` in the new session before running the original command. Within one session, rerunning skips the IDs already saved. If the upstream base has advanced, pass `--base` and `--revision` from the saved metadata to resume on the original model.
4. On the Mac, place the three JSONL files in `runs/finetune/`. Run these commands when ready to judge the results. The judge command uses the study’s normal judge provider.

   ```sh
   python3 score.py runs/finetune
   python3 judge.py runs/finetune
   python3 analyze.py runs/finetune --partial
   python3 robust.py runs/finetune --partial
   python3 scripts/compare_arms.py
   ```

The two partial reports go under `analysis/partial/finetune/`. The matched exploratory comparison goes to `analysis/finetune/compare.md`.

[Kaggle datasets](https://www.kaggle.com/docs/datasets) · [Kaggle notebooks](https://www.kaggle.com/docs/notebooks) · [Kaggle dataset size announcement](https://www.kaggle.com/discussions/product-announcements/512322) · [PyTorch CUDA builds](https://pytorch.org/get-started/previous-versions/) · [Qwen3.5 model implementation](https://huggingface.co/docs/transformers/model_doc/qwen3_5)
