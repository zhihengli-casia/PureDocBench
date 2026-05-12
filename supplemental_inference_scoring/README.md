# Supplemental Inference And Scoring Toolkit

This directory contains sanitized code from an internal PureDocBench inference/scoring workspace. It complements `model_inference/` with additional local and API model runners, post-processing scripts, scoring wrappers, model/config manifests, prompts, and environment freeze references.

Included:

- `tools/model_infer/`: standalone local model inference scripts.
- `tools/api_infer/`: API-backed inference clients that read provider credentials from environment variables.
- `tools/post_process/`: prediction cleanup utilities.
- `scripts/_runner/`: batch launchers for clean, degraded, and real-image tracks.
- `scoring/`: OmniDocBench wrapper scripts and YAML configs.
- `configs/`, `prompts/`, `repro/envs/`: model manifests, prompts, and environment references.

Excluded:

- `.env` and any real credentials.
- Logs, predictions, smoke-test outputs, incoming result drops, caches, and generated analysis artifacts.
- Model weights and private runtime directories.

Anonymization notes:

- Server paths were replaced by environment-variable placeholders such as `PDB_DATASET_ROOT`, `PDB_MODEL_ROOT`, `PDB_ENV_ROOT`, `PDB_SUPPLEMENTAL_ROOT`, `OMNIDOCBENCH_ROOT`, and `PDB_TMPDIR`.
- API scripts require provider credentials to be supplied by the user through local environment variables, for example `SILICONFLOW_API_KEY`.
- The files are provided for reproducibility and inspection; large data assets and model weights are not redistributed here.
