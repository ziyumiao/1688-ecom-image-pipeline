# CodesOnline Image API

Source: https://image.codesonline.dev/personal/docs (read 2026-07-27)

## Connection

- Base URL: `https://image.codesonline.dev/v1`
- Authentication: `Authorization: Bearer <API key>`
- Default model: `gpt-image-2`
- Text-to-image: `POST /v1/images/generations`
- Image editing: `POST /v1/images/edits`

## Shared parameters

- `model` (required): normally `gpt-image-2`
- `prompt` (required)
- `n`: 1-4, default 1
- `size`: ratio or dimensions, such as `1:1`, `16:9`, or `1024x1024`
- `quality`: `high`, `medium`, or `low`
- `style`: `natural` or `vivid`
- `background`: `opaque`, `transparent`, or `auto`
- `response_format`: `url` or `b64_json`; default `url`
- `upscale`: `2k` (long edge about 2560) or `4k` (long edge about 3840)

For edits, send multipart form data. `image` is the main required reference. Additional files may use `image[]`; at most 10 images and 100 MB total. `mask` is accepted but currently treated as another upstream reference.

## Recommended sizes

- Square: `1:1` or `1024x1024`
- Landscape: `16:9`, `3:2`, `4:3`, `1792x1024`, or `1536x1024`
- Portrait: `9:16`, `3:4`, `4:5`, `2:3`, `1024x1792`, or `1024x1536`

Always send `size` when the ratio matters.

## Responses

With `response_format=url`, read `data[].url`. A response may also include `fallback_url` and route-specific values under `data[].urls`. Signed URLs expire, so download immediately for long-term storage.

With `response_format=b64_json`, decode `data[].b64_json`.
