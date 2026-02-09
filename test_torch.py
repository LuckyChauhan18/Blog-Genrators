print("Testing torch import...")
try:
    import torch
    print(f"✅ torch imported: {torch.__version__}")
except Exception as e:
    print(f"❌ torch failed: {e}")
