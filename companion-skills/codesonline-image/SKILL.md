---
name: codesonline-image
description: Generate or edit bitmap images through the image.codesonline.dev OpenAI-compatible API. Use when the user explicitly invokes $codesonline-image or asks to use CodesOnline/image.codesonline.dev for text-to-image, image-to-image editing, transparent-background assets, ecommerce images, posters, or saving generated images locally. Do not use this skill for requests that do not specify CodesOnline unless the user has established it as their preferred image provider.
---

# CodesOnline Image

Use the bundled `scripts/generate_image.py` to call the service and save results locally.

## Workflow

1. Turn the user's request into a complete image prompt. Preserve all stated constraints. Add useful visual detail only when it does not change intent.
2. Choose text-to-image when no reference image is supplied. Choose image editing when one or more reference images are supplied.
3. Read the API key only from `CODESONLINE_IMAGE_API_KEY`. Never place it in prompts, files, logs, or the final response.
4. Run the script from the user's current working directory so relative output paths land there.
5. Prefer `quality=high`. Use `style=natural` for photography, products, architecture, and interiors; use `style=vivid` for posters, advertising, illustration, and stylized art.
6. Pass `--size` explicitly whenever aspect ratio matters. Do not rely on aspect-ratio wording in the prompt alone.
7. Inspect the saved image before presenting it. If it is visibly broken or misses an objective requirement, revise the prompt and retry once when reasonable.
8. Return a clickable absolute path and render the image in the response when supported.

## Commands

Text-to-image:

```powershell
python "<skill-dir>\scripts\generate_image.py" --prompt "..." --size "1:1" --quality high --style natural --output ".\generated.png"
```

Image editing:

```powershell
python "<skill-dir>\scripts\generate_image.py" --prompt "..." --image ".\reference.png" --size "1:1" --output ".\edited.png"
```

Multiple references:

```powershell
python "<skill-dir>\scripts\generate_image.py" --prompt "..." --image ".\main.png" --image ".\reference-2.png" --output ".\result.png"
```

Use `--background transparent` for cutouts or transparent assets. Use `--upscale 2k` or `--upscale 4k` only when the user needs a larger delivered file; this is interpolation, not AI super-resolution.

For full parameters, limits, and response behavior, read [references/api.md](references/api.md).

## Failure handling

- If `CODESONLINE_IMAGE_API_KEY` is absent, ask the user to set it in the environment. Do not ask them to paste the key into chat.
- Surface concise API error messages without exposing headers or credentials.
- If a signed result URL cannot be downloaded, retry with `--response-format b64_json`.
- Do not claim successful generation unless a non-empty image file exists.
