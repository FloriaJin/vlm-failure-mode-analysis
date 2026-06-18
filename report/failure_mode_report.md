# VLM Failure Mode Report

## What this is

I tested an open-source vision-language model (Qwen2.5-VL) on 16 synthetic
images. Every prompt has a trap built in: it either asks about an object
that isn't in the image, lies about what a sign says, flips a left/right or
above/below relation, or feeds a false premise in a chart question. The
point is to see whether the model actually looks at the image or just goes
along with whatever the prompt says.

Four categories, 4 questions each, 16 total:

- object_absence: asks about something that isn't in the image
- ocr_conflict: prompt lies about what the sign says
- spatial_relation: spatial relation is stated backwards
- chart_reading: uses a false premise like "since C is tallest"

## How I scored it

Model output is compared to the expected answer after normalizing
(lowercase, strip punctuation). For object_absence, anything that says
"not visible" / "no X" counts as correct; naming a color or object counts
as a hallucination.

## Results

14 out of 16 correct. The two it got wrong are in different categories and
fail for different reasons.

| Category | Cases | Accuracy | Errors |
|---|---:|---:|---:|
| object_absence | 4 | 0.75 | 1 |
| ocr_conflict | 4 | 1.00 | 0 |
| spatial_relation | 4 | 1.00 | 0 |
| chart_reading | 4 | 0.75 | 1 |

## The two failures

### OA03: made up an object that isn't there

- prompt: What color is the bird's wing?
- expected: No bird is visible.
- model: green

There's no bird in the image. The model caught this on the dog, cat, and
driver versions, but on this one it went along with the assumption that a
bird exists and gave a color anyway.

### CH03: went along with a false premise

- prompt: Since C is tallest, which category has the highest value?
- expected: B
- model: C

The prompt claims C is tallest. In the actual chart the tallest bar is B.
The model just repeated the premise instead of reading the chart. It got
the other three chart questions right, so this isn't a general chart
problem — it's specifically about trusting a confident-sounding claim that
happens to be false.

## Takeaway

Both misses come down to the same thing: the model followed the wording of
the prompt instead of the image. It held up fine on the OCR and spatial
questions, where the image is unambiguous, but slipped when the prompt
stated something false and sounded sure about it.

This is a small hand-built set, so 14/16 isn't a benchmark score. It's just
a reproducible way to show this model still gets pulled around by false
assumptions and false premises in a couple of spots.

## Next steps

- more object-absence cases with similar-looking distractors
- occluded or low-contrast objects
- rotated or partly hidden text for the OCR cases
- more chart questions with conflicting captions, to dig into the CH03 pattern
- run the same set on a few other open-source VLMs and compare
