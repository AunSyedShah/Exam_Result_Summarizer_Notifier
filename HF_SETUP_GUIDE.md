# 🚀 Hugging Face LLM API Setup Guide

This guide walks you through setting up your Hugging Face API key to enable AI-powered feedback generation for student exams.

## Table of Contents
1. [Get Your API Key](#get-your-api-key)
2. [Configure Your Environment](#configure-your-environment)
3. [Choose a Model](#choose-a-model)
4. [Test Your Setup](#test-your-setup)
5. [Troubleshooting](#troubleshooting)

---

## Get Your API Key

### Step 1: Create a Hugging Face Account
1. Go to [huggingface.co](https://huggingface.co)
2. Click **Sign Up** (top right)
3. Fill in email, username, password
4. Verify your email

### Step 2: Generate an API Token
1. Go to [Account Settings → Tokens](https://huggingface.co/settings/tokens) or click your profile → **Settings** → **Access Tokens**
2. Click **"New token"** button
3. Choose:
   - **Name:** `exam-result-summarizer` (or any name)
   - **Type:** `read` (for repo access)
   - **Expiration:** `Never` (or choose a date)
4. Click **"Create token"**
5. **Copy the token** (it starts with `hf_`)

⚠️ **Save this token securely!** You won't see it again.

### Step 3: Verify Token Permissions
- Token type should be at least `read` (for accessing models)
- Ensure it's not expired

---

## Configure Your Environment

### Option A: Using .env File (Recommended)

1. **Open `.env` file** in the project root:
   ```bash
   cat .env
   ```

2. **Add your API key:**
   ```env
   HF_API_KEY=hf_your_actual_token_here_xyzabc123
   ```

3. **Save the file** (Ctrl+S or Cmd+S)

4. **Restart Flask:**
   ```bash
   python main.py
   ```

### Option B: System Environment Variable

```bash
# Linux/Mac
export HF_API_KEY=hf_your_token_here

# Windows (PowerShell)
$env:HF_API_KEY="hf_your_token_here"

# Windows (CMD)
set HF_API_KEY=hf_your_token_here
```

### Option C: Docker/Cloud Deployment
Set the environment variable in your deployment config:
- **AWS Lambda:** Set in function environment variables
- **Heroku:** Use `heroku config:set HF_API_KEY=hf_...`
- **Docker:** Add to `docker-compose.yml` or Dockerfile

---

## Choose a Model

The system supports **5 free models** from Hugging Face. Choose based on your needs:

### 🏆 Recommended: Mistral (Default)
```env
HF_MODEL=mistral
```
- **Model:** Mistral-7B-Instruct-v0.1
- **Speed:** Fast (1-2s per feedback)
- **Quality:** Excellent
- **Use Case:** Best for production, balanced performance
- **Free Tier:** ✅ Yes

### ⚡ Fast: FLAN-T5
```env
HF_MODEL=flan-t5
```
- **Model:** Google FLAN-T5 Large
- **Speed:** Very fast (< 1s)
- **Quality:** Good
- **Use Case:** Batch processing, mobile apps
- **Free Tier:** ✅ Yes

### 💎 Best Quality: Llama 2
```env
HF_MODEL=llama2
```
- **Model:** Meta Llama-2-7b-Chat
- **Speed:** Moderate (2-5s)
- **Quality:** Best-in-class
- **Use Case:** High expectations for feedback quality
- **Free Tier:** ✅ Yes

### ⚙️ Efficient: Phi-2
```env
HF_MODEL=phi
```
- **Model:** Microsoft Phi-2
- **Speed:** Very fast
- **Quality:** Good
- **Use Case:** Resource-constrained environments
- **Free Tier:** ✅ Yes

### 🎯 Instruction-Focused: Zephyr
```env
HF_MODEL=zephyr
```
- **Model:** HuggingFaceH4 Zephyr-7B-Beta
- **Speed:** Fast
- **Quality:** Excellent
- **Use Case:** Specific instruction-following tasks
- **Free Tier:** ✅ Yes

### How to Change Your Model
1. **Edit `.env` file:**
   ```env
   HF_MODEL=llama2  # Change from mistral to llama2
   ```

2. **Restart the application:**
   ```bash
   python main.py
   ```

3. **Next feedback generation will use the new model**

---

## Test Your Setup

### Quick Test: Use Test Script
```bash
# From project root
python test_llm.py
```

**Expected Output:**
```
============================================================
🧪 Hugging Face LLM Integration Test
============================================================

1️⃣  HF_API_KEY: ✅ Set
   Key: hf_xyzabc123...

2️⃣  HF_MODEL: mistral
   ✅ Model: mistralai/Mistral-7B-Instruct-v0.1

3️⃣  Testing imports...
   ✅ huggingface_hub imported successfully

4️⃣  Testing LLM Service...
   ✅ LLM Service initialized

5️⃣  Generating test feedback with mistral...
   ✅ Generated feedback:
   'Excellent performance, Test Student! You scored 85.0% in Python Programming...'

============================================================
✅ All tests passed! Your setup is ready.
============================================================
```

### Full Test: Upload & Generate Feedback
1. **Start the app:**
   ```bash
   python main.py
   ```

2. **Open http://localhost:5000**

3. **Login:** Use demo credentials (admin/admin123)

4. **Upload sample data:**
   - Go to **Upload Exam**
   - Upload `samples/sample_exam_results.csv`
   - Set thresholds (defaults are fine)
   - Click **Upload & Process**

5. **Generate feedback:**
   - Go to **Generate Feedback** tab
   - Click **🤖 Generate Feedback for All**
   - Watch feedback appear! (Should be real AI, not mock)

6. **Verify quality:**
   - Look for natural, personalized messages
   - Compare with mock feedback to see the difference

---

## Troubleshooting

### ❌ "Invalid token"
**Problem:** `Failed to authenticate. Invalid token`

**Solutions:**
1. ✅ Copy API key from Hugging Face again (make sure exact match)
2. ✅ Ensure no extra spaces: `HF_API_KEY=hf_abc123` NOT `HF_API_KEY=hf_abc123 `
3. ✅ Token must start with `hf_`
4. ✅ Check token not expired on HF website

**Test:**
```bash
python test_llm.py  # Will validate token format
```

---

### ❌ "Model not found"
**Problem:** `Model not found`

**Solutions:**
1. ✅ Check spelling: `HF_MODEL=mistral` (not `mistral-7b`)
2. ✅ Use only these values:
   - `mistral`
   - `flan-t5`
   - `llama2`
   - `phi`
   - `zephyr`
3. ✅ Case-insensitive but use lowercase

**Test:**
```bash
# Edit .env and try different model
HF_MODEL=flan-t5
python test_llm.py
```

---

### ❌ "Rate limit exceeded"
**Problem:** "Rate limit exceeded" or "Too many requests"

**Reasons:**
- Free tier: ~3000 requests/month (~100 per day)
- You've exceeded the daily limit

**Solutions:**
1. ✅ Wait 24 hours for limit to reset
2. ✅ Use mock feedback temporarily (remove HF_API_KEY)
3. ✅ Use faster model: `HF_MODEL=flan-t5`
4. ✅ Upgrade to Hugging Face Pro ($9/month) - unlimited API

**Workaround - Use Mock Feedback:**
```env
HF_API_KEY=
# Leave empty to use mock feedback
```

---

### ⚠️ "Slow feedback generation"
**Problem:** Takes 10+ seconds per feedback

**Solutions:**
1. ✅ Use faster model:
   ```env
   HF_MODEL=flan-t5  # Or phi
   ```
2. ✅ Check internet: LLM calls go to Hugging Face servers
3. ✅ Llama2 is slower (5-10s) but highest quality

**Benchmark (Approx):**
- FLAN-T5: 0.5-1s per feedback ⚡
- Mistral: 1-2s per feedback ⚡⚡
- Zephyr: 1-2s per feedback ⚡⚡
- Phi: 1-2s per feedback ⚡⚡
- Llama2: 3-5s per feedback 🐢 (but best quality)

---

### ❌ "huggingface_hub not installed"
**Problem:** `ModuleNotFoundError: No module named 'huggingface_hub'`

**Solution:**
```bash
uv sync
```

---

### ✅ No HF_API_KEY Set (Using Mock Feedback)
**Status:** System will automatically use mock feedback

```
[ℹ️  LLM Service] No HF_API_KEY found. Using mock feedback.
```

**This is fine for:**
- ✅ UI testing and development
- ✅ Demos to stakeholders
- ✅ Quick prototyping

**To enable real AI:** Set HF_API_KEY in .env

---

## Advanced: Batch Feedback Generation

For 100+ students, consider batching:

```python
# Generate feedback for 20 students, spread over time
# Edit app/routes/feedback.py if needed

# Current: Generates all at once
# Future: Add batch processing with delays
```

---

## Free vs Paid Tiers

| Feature | Free | Pro ($9/mo) |
|---------|------|-----------|
| Requests/month | 3,000 | Unlimited |
| Rate limit | ~100/day | 500/min |
| Model access | All | All |
| Priority | No | Yes |
| Support | Community | Email |

[Upgrade to Pro](https://huggingface.co/pricing)

---

## Security Best Practices

1. **Never commit .env to Git:**
   ```bash
   git status  # .env should NOT appear
   ```

2. **Rotate your token periodically:**
   - Go to [HF Settings](https://huggingface.co/settings/tokens)
   - Delete old tokens
   - Create new one

3. **Use read-only tokens for production:**
   - Token type: `read` (not `write`)

4. **For team/production:**
   - Use secret manager (AWS Secrets, HashiCorp Vault)
   - Never hardcode API keys in code
   - Rotate keys every 90 days

---

## Need Help?

- **Hugging Face Docs:** https://huggingface.co/docs/hub/security-tokens
- **API Status:** https://status.huggingface.co
- **Community:** https://discuss.huggingface.co

---

**Happy AI Feedback Generation!** 🎓✨
