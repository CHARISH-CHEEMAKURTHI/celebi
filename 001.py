# # ================= ALL-IN-ONE FIX CELL =================
# import os

# # Fix 1: torchaudio removed set_audio_backend
# !sed -i 's/torchaudio\.set_audio_backend("soundfile")/pass/g' /usr/local/lib/python3.12/dist-packages/torch_audiomentations/utils/io.py

# # Fix 2: piper-sample-generator rolled back to the old layout + voice model
# if not os.path.exists("/content/piper-sample-generator/generate_samples.py"):
#     !rm -rf /content/piper-sample-generator
#     !git clone https://github.com/rhasspy/piper-sample-generator /content/piper-sample-generator
#     !cd /content/piper-sample-generator && git checkout v2.0.0
# if not os.path.exists("/content/piper-sample-generator/models/en_US-libritts_r-medium.pt"):
#     !mkdir -p /content/piper-sample-generator/models
#     !wget -O /content/piper-sample-generator/models/en_US-libritts_r-medium.pt 'https://github.com/rhasspy/piper-sample-generator/releases/download/v2.0.0/en_US-libritts_r-medium.pt'

# # Fix 3 (the newest error): PyTorch 2.6 changed torch.load defaults
# !sed -i 's/torch\.load(model_path)/torch.load(model_path, weights_only=False)/g' /content/piper-sample-generator/generate_samples.py

# # Fix 4: Python 3.12-compatible phonemizer, then re-pin setuptools
# !pip install -q piper-phonemize-fix || pip install -q piper-phonemize-cross
# !pip install -q "setuptools==75.2.0"

# import piper_phonemize
# print("ALL PATCHES APPLIED ✓")

# !sed -i 's/torch\.load(checkpoint_path, map_location=device)/torch.load(checkpoint_path, map_location=device, weights_only=False)/g' /usr/local/lib/python3.12/dist-packages/dp/model/model.py
# print("phonemizer loader patched")

# !rm -f /content/my_custom_model/hey_celebi/*.npy
# print("stale feature files removed")

# !pip install -q soundfile
# !sed -i 's/info = torchaudio\.info(file_path)/import soundfile as _sf; _i = _sf.info(str(file_path)); info = type("Info", (), {"num_frames": _i.frames, "sample_rate": _i.samplerate})()/' /usr/local/lib/python3.12/dist-packages/torch_audiomentations/utils/io.py
# !grep -c "soundfile as _sf" /usr/local/lib/python3.12/dist-packages/torch_audiomentations/utils/io.py
# print("torchaudio.info patched")

# !pip install -q onnxscript
# print("onnxscript installed")

# # =======================================================





# import onnx
# m = onnx.load("/content/my_custom_model/hey_celebi.onnx")
# onnx.save_model(m, "/content/my_custom_model/hey_celebi_final.onnx", save_as_external_data=False)
# print("merged into hey_celebi_final.onnx")
