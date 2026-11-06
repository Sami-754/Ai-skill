---
name: convertx
description: Multi-format file conversion service supporting over 1,000 formats (documents, images, videos, audio, ebooks, vector, 3D, LaTeX, archives). Use when the user wants to convert files locally, inspect supported conversion formats, or start and control the self-hosted ConvertX daemon.
---

# ConvertX File Converter

`convertx` provides local, self-hosted file conversion across 1,000+ formats powered by industry-standard engines (FFmpeg, LibreOffice, ImageMagick, Pandoc, Calibre, Inkscape, Resvg, Potrace, Assimp, Vips, and Markitdown).

---

## 1. Quick CLI Management

Manage the native ConvertX daemon using the global executable:

```bash
convertx status    # Check daemon process and HTTP health
convertx start     # Start daemon in background (Native Bun)
convertx stop      # Stop daemon
convertx restart   # Restart daemon
convertx logs      # Tail recent service logs
convertx url       # Print the web UI URL (http://localhost:8383)
convertx open      # Open in browser
```

- **Service URL**: `http://localhost:8383`  
- **Executable**: `~/.local/bin/convertx` (wraps `~/.local/share/convertx/convertx`)  
- **Persistent Data & DB**: `~/.local/share/convertx/data/` (SQLite: `mydb.sqlite`)  
- **Runtime**: Native Bun binary on CachyOS (zero Docker overhead, instant startup)  

---

## 2. Converting Files

### Option A: Web Interface
1. Run `convertx start` (if not already running).
2. Open `http://localhost:8383` in your browser.
3. Drag & drop files, select target format, and click Convert.

### Option B: Programmatic HTTP API
ConvertX exposes an internal Elysia API:
- `GET /healthcheck` -> `{ "status": "ok" }`
- `GET /api/converters` -> List all active converters and formats
- `POST /upload` -> Upload source file for conversion
- `POST /convert` -> Trigger format conversion job

---

## 3. Supported Format Engines

| Engine | Domains | Converts From | Converts To |
| :--- | :--- | :---: | :---: |
| **FFmpeg** | Video / Audio / Animation | ~472 formats | ~199 formats |
| **ImageMagick** | Raster Images | 245 formats | 183 formats |
| **GraphicsMagick** | High-performance Raster Images | 167 formats | 130 formats |
| **Pandoc** | Markdown, DOCX, EPUB, PDF, HTML | 43 formats | 65 formats |
| **LibreOffice** | Office Documents (Word, Excel, PPT) | 41 formats | 22 formats |
| **Calibre** | E-books (EPUB, MOBI, AZW3, PDF) | 26 formats | 19 formats |
| **Inkscape / Resvg** | Vector Graphics (SVG, AI, CDR, EPS) | 8 formats | 18 formats |
| **Assimp** | 3D Assets (OBJ, FBX, STL, GLTF, DAE) | 77 formats | 23 formats |
| **Potrace / VTracer**| Raster-to-Vector Tracing | 12 formats | 12 formats |
| **XeLaTeX** | LaTeX compilation | 1 format | PDF / PostScript |
| **Markitdown** | AI-optimized document conversion | 6 formats | Markdown |

For detailed format mappings, see [converters reference](references/converters.md).
