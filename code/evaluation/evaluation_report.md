# Evaluation Report

## Model

OpenRouter Vision Model:

google/gemini-2.5-flash

## Dataset

* Sample dataset: 20 claims
* Test dataset: 44 claims

## Processing Strategy

For each claim:

1. Parse claim conversation.
2. Load all referenced images.
3. Send claim text and images to the vision model.
4. Receive structured JSON response.
5. Normalize outputs to the required schema.
6. Write final prediction row.

## Approximate Model Calls

* Sample evaluation: 20 calls
* Test generation: 44 calls
* Total: approximately 64 calls

One model call is used per claim.

## Images Processed

Images per claim:

* Minimum: 1
* Maximum: 3

Estimated totals:

* Sample dataset: ~40 images
* Test dataset: ~90 images
* Total processed: ~130 images

## Approximate Token Usage

Estimated per claim:

* Input prompt: 800–1200 tokens
* Output JSON: 100–300 tokens

Estimated total:

* Input tokens: ~60,000
* Output tokens: ~10,000

Actual usage varies depending on image count and conversation length.

## Cost Estimate

Pricing depends on the selected OpenRouter model and image-processing charges.

Assumptions:

* 64 model calls
* Approximately 130 images processed
* Lightweight vision model (Gemini Flash)

Estimated total cost is low and suitable for evaluation-scale workloads.

## Runtime

Observed runtime:

* Approximately one model call per claim
* Sequential execution

Estimated end-to-end runtime:

* Sample dataset: 1–2 minutes
* Test dataset: 2–5 minutes

Actual runtime depends on network latency and API response times.

## TPM / RPM Considerations

The implementation uses sequential processing.

Advantages:

* Avoids rate-limit spikes
* Reduces API throttling risk
* Simplifies error handling

For larger datasets, batching or controlled concurrency could be added.

## Batching, Throttling, and Retry Strategy

Current implementation:

* No batching
* No parallel execution
* Sequential requests

Potential improvements:

* Retry on transient API failures
* Exponential backoff
* Request queue for high-volume processing
* Local caching of previously processed images

## Caching

No persistent cache is implemented.

Each claim is evaluated independently.

## Operational Notes

The solution prioritizes:

* simplicity
* reproducibility
* schema compliance
* low implementation complexity

while maintaining multimodal reasoning across images and claim conversations.
