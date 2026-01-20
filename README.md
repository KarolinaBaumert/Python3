<img width="1830" height="186" alt="image" src="https://github.com/user-attachments/assets/b08ee5a9-e207-4a5d-8cfc-5782f1d23755" />

## Photo Storage

This system supports two ways to analyze images:

### 1. URL-based Analysis (existing)
Submit an image by providing a URL to an externally hosted image:
```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/image.jpg"}'
```

### 2. File Upload (new)
Upload an image file directly to the system. The photo will be stored on the server:
```bash
curl -X POST http://localhost:8001/analyze/upload \
  -F "file=@/path/to/your/image.jpg"
```

**How photos are stored:**
- Uploaded photos are stored in the `/app/uploads` directory inside the container
- On the host machine, photos are persisted in the `./uploads` directory
- Each photo is saved with a unique filename based on the job ID
- The original file extension is preserved
- Photos are accessible to both the API and worker services via shared volume

<img width="1830" height="227" alt="image" src="https://github.com/user-attachments/assets/b520ac35-8606-42e0-ae3a-9e48069f5735" />

<img width="1829" height="227" alt="image" src="https://github.com/user-attachments/assets/8cd6677f-17d5-427c-b7c3-a8a90cf5282e" />

<img width="1825" height="229" alt="image" src="https://github.com/user-attachments/assets/eea415ea-3e1c-44b6-ab2c-3dd0bd5aa556" />

<img width="483" height="418" alt="image" src="https://github.com/user-attachments/assets/c8466f43-f062-4fb6-9688-a26a4ff111e4" />

<img width="1832" height="356" alt="image" src="https://github.com/user-attachments/assets/4cac5d21-4087-4835-aa49-246a2ffc4f10" />

<img width="842" height="288" alt="image" src="https://github.com/user-attachments/assets/9519caa5-bebd-4af8-be13-1a5c9b01c019" />

<img width="874" height="340" alt="image" src="https://github.com/user-attachments/assets/9da891e4-114e-4c1d-8930-693ca276b6c4" />

