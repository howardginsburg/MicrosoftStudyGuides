# AI-103 Domain 4 — Source pack (public Microsoft Learn only)

> **Exam weight:** 10–15%  
> **Domain:** Implement text analysis solutions  
> All bullets are paraphrased from public Microsoft Learn documentation. No verbatim copy, no third-party sources.

---

## o-4-1-1 Extract entities, topics, summaries, and structured JSON outputs

- **Named Entity Recognition (NER)** in Azure AI Language identifies and categorizes entities—people, places, organizations, and quantities—in unstructured text using a preset entity list; the *custom NER* variant lets you train a model to recognize domain-specific entity types.
- **Azure AI Language Summarization** delivers three genre-specific summarization modes: *text* (plain text blocks), *conversation* (multi-turn transcripts with recap/issue-resolution/chapter-title/narrative aspects), and *native document* (.txt, .pdf, .docx)—each via REST API or SDK.
- **Extractive summarization** selects and ranks the most salient original sentences (returns rank score and positional info); **abstractive summarization** generates concise, novel sentences not verbatim from the source—both return results within 24 hours before output is purged.
- **Azure OpenAI Structured Outputs** enforces strict JSON Schema adherence by setting `response_format` to `json_schema` with `strict: true`; unlike the older JSON mode (which guarantees valid JSON but not schema shape), structured outputs guarantee schema compliance—useful for function calling, entity extraction, and multi-step pipelines.
- Structured outputs require API version **2024-08-01-preview** or later (GA: **2024-10-21**); supported models include `gpt-4o` (2024-08-06+), `gpt-4o-mini` (2024-07-18), `gpt-4.1`, `o4-mini`, `o3`, and others—but **not** `gpt-4o-audio-preview`.
- Structured outputs are **not** supported with bring-your-own-data scenarios, Assistants API, or Azure AI Agents Service.
- The Python `openai` + `pydantic` stack lets you declare a `BaseModel` schema (e.g., fields `title`, `summary`, `tags`) and pass it as the response format; the SDK validates the response against the model before returning it.

```python
from pydantic import BaseModel, Field
from openai import AzureOpenAI

class ArticleSummary(BaseModel):
    title: str
    summary: str = Field(..., description="1-2 sentence summary")
    entities: list[str] = Field(..., description="Named entities mentioned")

client = AzureOpenAI(azure_endpoint="<endpoint>", api_key="<key>", api_version="2024-10-21")
completion = client.beta.chat.completions.parse(
    model="gpt-4o",  # deploy name
    messages=[{"role": "user", "content": "Summarize: <article text>"}],
    response_format=ArticleSummary,
)
result: ArticleSummary = completion.choices[0].message.parsed
```

Sources:
- https://learn.microsoft.com/azure/ai-services/language-service/named-entity-recognition/overview
- https://learn.microsoft.com/azure/ai-services/language-service/summarization/overview
- https://learn.microsoft.com/azure/ai-foundry/openai/how-to/structured-outputs
- https://learn.microsoft.com/azure/foundry/openai/how-to/json-mode
- https://learn.microsoft.com/azure/developer/ai/how-to/extract-entities-using-structured-outputs

---

## o-4-1-2 Detect sentiment, tone, safety issues, and sensitive content (incl. PII detection)

- **Sentiment Analysis** assigns *positive*, *neutral*, or *negative* labels at both the sentence level and the document level, returning confidence scores between 0 and 1 for each label; the label chosen is the one with the highest score.
- **Opinion Mining** (also called aspect-based sentiment analysis) links detected sentiments to specific words or attributes (e.g., a product feature), providing more granular insight than document-level sentiment alone.
- **PII Detection** in Azure AI Language offers three feature types matched to input format: *Text PII* for synchronous string payloads (messages, prompts, logs); *Conversation PII* for turn-based chat/transcript structures; and *Document-based PII* for asynchronous processing of `.pdf`, `.docx`, and `.txt` files that preserves document structure.
- All PII feature types return structured output with entity categories, confidence scores, and redacted results configurable by masking style; common use cases include redacting call-center transcripts, preparing ML training data, and applying sensitivity labels.
- Sentiment analysis and classic Language summarization are scheduled to **retire March 31, 2029**; Microsoft recommends migrating new projects to Azure AI Foundry models for enhanced NLU capabilities.
- Both sentiment analysis and PII detection can be deployed as **Docker containers** for on-premises workloads where compliance or data residency requirements prevent cloud processing.
- All Azure Language features use the shared `azure-ai-textanalytics` (Python) / `Azure.AI.TextAnalytics` (.NET) SDK and can be combined in a single async batch request.

```python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

client = TextAnalyticsClient("<endpoint>", AzureKeyCredential("<key>"))

# Sentiment
docs = ["The service was fast but the interface was confusing."]
result = client.analyze_sentiment(docs, show_opinion_mining=True)
for doc in result:
    print(doc.sentiment, doc.confidence_scores)  # e.g. mixed, positive=0.7

# PII redaction
pii_result = client.recognize_pii_entities(["Call John Smith at 555-123-4567."])
for doc in pii_result:
    print(doc.redacted_text)  # "Call ********* at ************."
```

Sources:
- https://learn.microsoft.com/azure/ai-services/language-service/sentiment-opinion-mining/overview
- https://learn.microsoft.com/azure/ai-services/language-service/personally-identifiable-information/overview

---

## o-4-1-3 Translate text via Azure Translator in Foundry Tools or LLM-powered translation flows

- **Azure Translator in Foundry Tools** is a cloud-based neural machine translation (NMT) service; the **2026-06-06 GA API** adds the ability to optionally select a large language model (e.g., `GPT-5.4`) per request in place of, or alongside, the standard NMT path.
- LLM translation requires a **Foundry resource** (not just a classic Translator resource); NMT continues to work with existing Translator or multi-service resources inside the Foundry portal.
- **Service limits differ by path**: NMT allows up to 1,000 array elements / 50,000 characters per element; LLM translation is capped at 50 array elements / 5,000 characters per element—design routing rules accordingly.
- **Billing also differs**: NMT is billed by source-text character count; LLM translation is billed by processed input and output tokens (Azure OpenAI pricing).
- The Foundry portal Translator playground (November 2025+) lets you pick from three model options—*Azure-MT* (NMT), *GPT-4o*, and *GPT-4o mini*—and tailor translations by gender, tone, or domain-specific terminology without writing code.
- The **Transliterate** operation maps a source language script or alphabet to a target script (e.g., Japanese kana → Latin romanization) and is available alongside translate and language-detection endpoints.
- For high-volume baseline traffic with cost sensitivity, route to NMT; reserve LLM translation for scenarios requiring adaptive behavior, tone control, or richer contextual handling.

```python
import requests, uuid

endpoint = "https://api.cognitive.microsofttranslator.com"
headers = {
    "Ocp-Apim-Subscription-Key": "<key>",
    "Ocp-Apim-Subscription-Region": "<region>",
    "Content-Type": "application/json",
    "X-ClientTraceId": str(uuid.uuid4()),
}
body = [{"text": "Ciao"}]
params = {"api-version": "3.0", "from": "it", "to": ["en", "fr"]}
response = requests.post(f"{endpoint}/translate", headers=headers, params=params, json=body)
print(response.json())  # [{"translations": [{"text": "Hello", "to": "en"}, ...]}]
```

Sources:
- https://learn.microsoft.com/azure/ai-services/translator/overview
- https://learn.microsoft.com/azure/ai-services/translator/text-translation/overview
- https://learn.microsoft.com/azure/ai-services/translator/text-translation/2026-06-06/rest-api-guide
- https://learn.microsoft.com/azure/ai-services/translator/whats-new

---

## o-4-1-4 Customize language model outputs for domain tasks (compliance summarization, domain extraction)

- **Custom NER** allows you to label and train a model on domain-specific entities not covered by the prebuilt NER entity list (e.g., contract clause types, medical drug names); training requires labeled examples in Language Studio or via REST API.
- **Custom Translator** lets you train domain-adapted MT models using parallel bilingual document pairs; once trained, the model is assigned a *Category ID* that can be passed in Translator API calls to route requests through the custom model.
- **Adaptive custom translation** (available in the 2026-06-06 API for select language pairs including English, French, German, Spanish) lets you fine-tune translation behavior using domain-specific terminology without full retraining.
- **Azure AI Language Summarization** can be configured for conversation-specific aspects—*recap*, *issue/resolution* (call center), *chapter title*, and *narrative*—making it suitable for compliance call logging, meeting notes, and audit-trail summarization workflows.
- **Structured outputs with Pydantic schemas** enforce domain-specific JSON shapes from generative models: define a `BaseModel` with fields like `clause_type`, `risk_level`, and `summary`, then pass it as `response_format` to ensure the LLM returns data in a machine-consumable structure for downstream compliance pipelines.
- The `azure-ai-textanalytics` SDK's `analyze_actions` method lets you combine multiple Language actions (NER, summarization, key phrase extraction, PII redaction) in a single asynchronous batch request—important for throughput-sensitive compliance workflows.
- Document-based summarization and PII detection support native `.pdf` and `.docx` inputs, eliminating preprocessing steps in document-heavy compliance use cases.

```python
from azure.ai.textanalytics import (
    TextAnalyticsClient, ExtractSummaryAction, RecognizeEntitiesAction
)
from azure.core.credentials import AzureKeyCredential

client = TextAnalyticsClient("<endpoint>", AzureKeyCredential("<key>"))
docs = ["This agreement shall remain in force for a period of three years..."]

poller = client.begin_analyze_actions(
    docs,
    actions=[
        ExtractSummaryAction(max_sentence_count=3),
        RecognizeEntitiesAction(),
    ],
)
for result_page in poller.result():
    for result in result_page:
        print(result)
```

Sources:
- https://learn.microsoft.com/azure/ai-services/language-service/named-entity-recognition/overview
- https://learn.microsoft.com/azure/ai-services/language-service/summarization/overview
- https://learn.microsoft.com/azure/ai-services/translator/overview
- https://learn.microsoft.com/azure/ai-foundry/openai/how-to/structured-outputs

---

## o-4-2-1 Convert speech to text and text to speech for agentic interactions (Azure AI Speech SDK)

- The **Azure AI Speech SDK** exposes speech-to-text (STT), text-to-speech (TTS), speech translation, and related capabilities; it is available for C#, C++, Java, JavaScript, Python, Go, Objective-C, and Swift across Windows, Linux, macOS, Android, iOS, and browser environments.
- For **real-time STT**, create a `SpeechRecognizer` from a `SpeechConfig` (endpoint + key) and an `AudioConfig` (microphone or file); call `recognize_once_async()` for single utterances or use continuous recognition events for streaming agent interactions.
- For **TTS**, create a `SpeechSynthesizer` with a `SpeechConfig` specifying voice name and language; call `speak_text_async()` to generate audio output—suitable for agent response playback in voice-first interfaces.
- For batch transcription and custom speech model management, use the **Speech REST API** rather than the SDK; for LLM-enhanced and fast transcription scenarios, use the separate **Speech Transcription SDK** (`azure-ai-speech-transcription` package).
- The Speech SDK handles both real-time (streaming microphone input) and non-real-time (file or Azure Blob Storage) scenarios with the same API surface, making it straightforward to switch modalities in agent pipelines.
- SDK samples are available in the `Azure-Samples/cognitive-services-speech-sdk` GitHub repository; language-specific reference docs are maintained per SDK (e.g., Python: `azure-cognitiveservices-speech`).

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(subscription="<key>", region="<region>")
speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

# Text-to-speech for agent response
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
result = synthesizer.speak_text_async("Agent response here.").get()

# Speech-to-text from microphone
recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
recognition = recognizer.recognize_once_async().get()
print(recognition.text)
```

Sources:
- https://learn.microsoft.com/azure/ai-services/speech-service/speech-sdk
- https://learn.microsoft.com/azure/ai-services/speech-service/overview

---

## o-4-2-2 Integrate speech as an agent modality, including custom speech models

- **Custom Speech** allows you to improve recognition accuracy beyond the universal base model by training on domain-specific vocabulary and audio conditions; inputs can include text transcripts, audio + reference transcriptions, structured text (for pattern-based domains), and custom pronunciations.
- The Custom Speech workflow: (1) create a project in Speech Studio or via API, (2) upload test data, (3) train a custom model, (4) evaluate accuracy with **Word Error Rate (WER)**, (5) deploy to a **custom endpoint**.
- Custom endpoints are required for real-time STT use of a custom model; batch transcription is the one exception—it can reference a custom model without a dedicated hosted endpoint to reduce cost.
- **Model stability**: a deployed custom endpoint remains fixed at its trained version until you explicitly update it; recognition accuracy and quality are consistent even when Microsoft releases newer base models—enabling predictable agent behavior.
- Training cost applies if the base model was created on or after October 1, 2023; endpoint hosting incurs an ongoing charge regardless of base model date.
- Multiple custom models are recommended when a domain spans sub-areas with distinct vocabulary (e.g., separate models per Olympic sport), as focused models outperform generalized ones on niche vocabulary.
- Custom speech models integrate with the standard Speech SDK—simply point `SpeechConfig.endpoint_id` at the custom endpoint URL; no SDK API changes required.

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(subscription="<key>", region="<region>")
# Point to a deployed custom speech endpoint
speech_config.endpoint_id = "<custom-endpoint-id>"

audio_config = speechsdk.AudioConfig(filename="domain_audio.wav")
recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
result = recognizer.recognize_once_async().get()
print(result.text)
```

Sources:
- https://learn.microsoft.com/azure/ai-services/speech-service/custom-speech-overview
- https://learn.microsoft.com/azure/ai-services/speech-service/how-to-custom-speech-train-model
- https://learn.microsoft.com/azure/ai-services/speech-service/speech-sdk

---

## o-4-2-3 Enable multimodal reasoning from audio inputs (audio-capable models)

- **GPT Realtime API** (part of the GPT-4o model family) supports low-latency "speech in, speech out" conversational interactions over a persistent WebSocket connection—ideal for customer support agents, voice assistants, and real-time translators.
- Audio-capable model deployments like **`gpt-4o-audio-preview`** and **`gpt-4o-mini-audio-preview`** accept audio as part of a multimodal chat message (alongside text and images), enabling models to reason over spoken content directly without separate STT preprocessing.
- **`gpt-realtime-translate`** is a dedicated Foundry model for real-time speech translation available as a Global Standard (pay-as-you-go) deployment; it is priced hourly under the Audio Models section of Azure OpenAI pricing.
- Important constraint: **structured outputs are not supported** with `gpt-4o-audio-preview` and `gpt-4o-mini-audio-preview` (version 2024-12-17)—if your pipeline requires schema-enforced JSON output, pre-process audio to text first, then apply structured outputs on the text response.
- The Realtime API uses a WebSocket-based protocol; the `openai` Python library provides a `RealtimeClient` helper for managing the session, sending audio deltas, and receiving transcription and response events.
- Audio model sessions can include transcription settings with an ISO-639-1 language hint (e.g., `"en"`) to improve accuracy; validate target language pairs with production-like audio before deployment.
- **LLM Speech** (Azure AI Speech Transcription SDK) provides LLM-enhanced transcription and translation across ~25 languages in multi-lingual mode by default; it operates as an alternative to the classic STT pipeline for higher-accuracy transcription without specifying an input locale.

```python
# Audio file input to gpt-4o for multimodal reasoning (non-realtime)
import base64
from openai import AzureOpenAI

client = AzureOpenAI(azure_endpoint="<endpoint>", api_key="<key>", api_version="2025-01-01-preview")

with open("audio_clip.wav", "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode()

response = client.chat.completions.create(
    model="gpt-4o-audio-preview",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Summarize the key points from this audio."},
            {"type": "input_audio", "input_audio": {"data": audio_b64, "format": "wav"}},
        ],
    }],
)
print(response.choices[0].message.content)
```

Sources:
- https://learn.microsoft.com/azure/ai-services/openai/realtime-audio-quickstart
- https://learn.microsoft.com/azure/foundry/openai/concepts/gpt-realtime-translate
- https://learn.microsoft.com/azure/ai-services/speech-service/llm-speech
- https://learn.microsoft.com/azure/ai-services/speech-service/overview

---

## o-4-2-4 Translate speech into other languages using language models and Foundry Tools

- **Azure AI Speech translation** provides real-time, multi-language speech-to-text and speech-to-speech translation using the Speech SDK or CLI; core features include STT translation, speech-to-speech synthesis, multi-lingual translation, Live Interpreter, and multiple target language output.
- The standard Speech Translation API natively supports up to **2 target languages** in a single call; producing output in more than two target languages requires a **multi-service Foundry resource** (or separate translation service calls), with Translator pricing applied per additional language.
- **Live Interpreter** continuously identifies the spoken language without requiring a pre-set input locale, delivering low-latency speech-to-speech translation in a natural synthesized voice that preserves the speaker's style and tone—designed for Teams meetings, international classrooms, contact centers, and global events.
- **Custom translation in speech**: Speech Translation integrates with Azure Custom Translator; supply the Custom Translator *Category ID* in your `SpeechTranslationConfig` to apply domain-adapted MT models (e.g., legal or medical terminology) to the translated output.
- **GPT Realtime Translate** (`gpt-realtime-translate`) is a Foundry model optimized for multilingual speech-to-speech translation, available as a Global Standard deployment; for production, validate language pairs against production-like audio before rollout.
- **LLM Speech** (Speech Transcription SDK) supports ~25 input languages for both transcribe and translate tasks, operating in multi-lingual mode by default with optional locale hints; use the `@azure/ai-speech-transcription` (Node) or `Azure.AI.Speech.Transcription` (.NET) packages.
- Billing combines STT transcription cost plus Translator character-based fees for each target language beyond the second; plan capacity and routing based on audio duration and character output estimates.

```python
import azure.cognitiveservices.speech as speechsdk

translation_config = speechsdk.translation.SpeechTranslationConfig(
    subscription="<key>", region="<region>"
)
translation_config.speech_recognition_language = "en-US"
translation_config.add_target_language("fr")   # target 1
translation_config.add_target_language("de")   # target 2 (within free tier)

audio_config = speechsdk.AudioConfig(use_default_microphone=True)
recognizer = speechsdk.translation.TranslationRecognizer(
    translation_config=translation_config, audio_config=audio_config
)

def handle_result(evt):
    for lang, text in evt.result.translations.items():
        print(f"[{lang}] {text}")

recognizer.recognized.connect(handle_result)
recognizer.start_continuous_recognition()
```

Sources:
- https://learn.microsoft.com/azure/ai-services/speech-service/speech-translation
- https://learn.microsoft.com/azure/ai-services/speech-service/how-to-translate-speech
- https://learn.microsoft.com/azure/ai-services/speech-service/get-started-speech-translation
- https://learn.microsoft.com/azure/foundry/openai/concepts/gpt-realtime-translate
- https://learn.microsoft.com/azure/ai-services/speech-service/llm-speech
