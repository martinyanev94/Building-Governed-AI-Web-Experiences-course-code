# Computer Vision Authentication

This bounded Python prototype evaluates the authentication boundary around a visual verification result. It does not implement facial recognition and does not provide production security evidence.

## Run

From the project directory:

```bash
python -m pytest
```

The tests cover verified, uncertain, preprocessing-failure, camera-unavailable, and image-retention boundary cases. The expected contract is that uncertain or failed visual processing uses a fallback path and that raw images are never retained.
