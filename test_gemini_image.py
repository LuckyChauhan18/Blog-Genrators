from gradio_client import Client
from pathlib import Path
import shutil

print("🔑 Hugging Face setup ready")

# 1️⃣ Create client FIRST
SPACE_ID = "hysts/SDXL"
client = Client(SPACE_ID)

print("Loaded as API:", client.src)
print("🎨 Generating image via Hugging Face Space...")

# 2️⃣ Call predict
result = client.predict(
    "image of transformer in a futuristic cityscape at sunset, vibrant colors, cinematic lighting, highly detailed",
    api_name="/predict",
)

print("🧠 Raw result:", result)

out = Path("hf_generated.webp")

# 3️⃣ Handle local temp file (your case)
if isinstance(result, str) and Path(result).exists():
    print("📁 Image returned as local temp file")
    shutil.copy(result, out)

else:
    raise RuntimeError("❌ Unexpected response format")

print("✅ IMAGE GENERATED SUCCESSFULLY")
print("📂 Saved at:", out.resolve())
print("📏 Size:", out.stat().st_size, "bytes")
