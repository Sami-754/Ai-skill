# ConvertX Converters & Formats Reference

## Converter Engine Breakdown

### 1. Document & Text
- **Pandoc**: Markdown, HTML, LaTeX, DocBook, OPML, Org-Mode, EPUB, DOCX, ODT, RTF, PPTX.
- **LibreOffice**: DOC, DOCX, XLS, XLSX, PPT, PPTX, ODT, ODS, ODP, RTF, TXT, PDF.
- **Markitdown**: Extracts clean Markdown from PDF, Word, PowerPoint, Excel, Images (with OCR), and Audio (transcription).
- **XeLaTeX**: Compile `.tex` documents with Unicode support into print-ready PDF.

### 2. Images & Vector
- **ImageMagick & GraphicsMagick**: PNG, JPG, JPEG, WEBP, GIF, TIFF, BMP, ICO, TGA, PSD, HDR, HEIC, AVIF, RAW.
- **libvips**: High-speed image processing and resizing.
- **Inkscape & resvg**: SVG, SVGZ, AI, EPS, PDF, PS.
- **Potrace & VTracer**: High-fidelity bitmap tracing (PNG/JPG to SVG/DXF/EPS).
- **libjxl & libheif**: Next-gen compression (JPEG XL, HEIC/HEIF).

### 3. Audio & Video
- **FFmpeg**: MP4, MKV, AVI, MOV, WEBM, FLV, WMV, MP3, WAV, FLAC, AAC, OGG, OPUS, M4A, GIF.
  - Video codec transcoding (H.264, H.265, AV1, VP9, ProRes).
  - Audio extraction, bitrate conversion, and channel remapping.

### 4. E-books & 3D Assets
- **Calibre**: EPUB, MOBI, AZW, AZW3, FB2, LIT, LRF, PDB, PML, RB, RTF, SNB, TCR, TXT, PDF.
- **Assimp**: 3D formats (OBJ, STL, DAE, FBX, GLTF, GLB, 3DS, BLEND, PLY, DXF).

---

## Configuration Variables (Daemon Environment)

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `PORT` | `8383` | Port for the web interface and API. |
| `HTTP_ALLOWED` | `true` | Allows local unencrypted HTTP connections (`http://localhost:8383`). |
| `ACCOUNT_REGISTRATION` | `true` | Allows user account registration. |
| `ALLOW_UNAUTHENTICATED` | `false` | When `true`, allows public access without login. |
| `AUTO_DELETE_EVERY_N_HOURS` | `24` | Auto-purges uploaded and converted temporary files. |
| `DB_PATH` | `./data/mydb.sqlite` | SQLite database path. |
