# Phronesis Logo Assets

Complete brand asset package for the Phronesis AI Agent Framework.

## Quick Start

### Essential Files
- `phronesis-master.svg` - Master source file (edit this, export everything else from it)
- `symbol/symbol.svg` - Standalone mark (most versatile)
- `lockup/lockup-horizontal-dark.svg` - Primary logo for dark backgrounds
- `lockup/lockup-horizontal.svg` - Primary logo for light backgrounds
- `favicon/favicon.svg` - Browser icon

## Directory Structure

```
assets/
├── phronesis-master.svg          # Master source (1024×1024)
├── symbol/                       # Mark only
│   ├── symbol.svg               # Black version
│   ├── symbol-light.svg         # White version
│   └── symbol-*.png            # Raster exports (16-1024px)
├── lockup/                      # Symbol + wordmark
│   ├── lockup-horizontal.svg    # Light background
│   ├── lockup-horizontal-dark.svg # Dark background
│   ├── lockup-horizontal-monochrome.svg # Single color
│   ├── lockup-vertical.svg      # Stacked layout
│   └── lockup-*.png            # Raster exports
├── favicon/                     # Browser icons
│   ├── favicon.svg             # Modern browsers
│   ├── favicon.ico             # Legacy (multi-res: 16, 32, 48)
│   ├── favicon-*.png           # Explicit sizes
│   ├── apple-touch-icon.png    # iOS bookmark (180×180)
│   └── safari-pinned-tab.svg   # Safari pinned tab
└── social/                      # Social media & platforms
    ├── og-image.png            # Open Graph (1200×630)
    ├── og-image-square.png     # Square variant (1200×1200)
    ├── github-social-preview.png # GitHub preview (1280×640)
    ├── avatar-512.png          # Profile picture (512×512)
    ├── android-chrome-192x192.png # Android home screen
    └── android-chrome-512x512.png # Android splash
```

## Usage Guidelines

### Symbol (Mark Only)
Use when space is limited or brand is already established:
- App icons
- Favicons
- Social media avatars
- Inline badges
- Small UI contexts

**Minimum size**: 16×16px (verify legibility)

### Lockup (Symbol + Wordmark)
Primary logo for headers, presentations, documentation:
- **Horizontal**: Default for most contexts
- **Vertical**: Square spaces, narrow columns
- **Dark variant**: Use on dark backgrounds (#2d2d2d or darker)
- **Light variant**: Use on white/light backgrounds
- **Monochrome**: Print, single-color reproduction

**Minimum legible width**: 120px for horizontal lockup

### Color Specifications
- **Primary Dark**: `#2d2d2d` (background)
- **Symbol/Text**: `#000000` (light bg) / `#ffffff` (dark bg)
- **Secondary Text**: `#666666` (light bg) / `#999999` (dark bg)

### Clear Space & Spacing
- Maintain minimum clear space around logo equal to the height of the symbol
- The lockup uses tight spacing between symbol and wordmark (no gap) for a unified, compact appearance
- "FRAMEWORK" subtitle is slightly offset to the right for visual balance

## Implementation

### HTML/Web
```html
<!-- Favicon -->
<link rel="icon" type="image/svg+xml" href="/assets/favicon/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/favicon/apple-touch-icon.png">

<!-- Open Graph -->
<meta property="og:image" content="/assets/social/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
```

### Python Package (PyPI)
Use `symbol-256.png` or `symbol-512.png` in your package README:
```markdown
![Phronesis](https://raw.githubusercontent.com/your-org/phronesis/main/assets/symbol/symbol-256.png)
```

### Documentation
Use lockup variants based on your theme:
```markdown
![Phronesis](./assets/lockup/lockup-horizontal.svg)
```

### GitHub
1. Repository Settings → Social Preview: Upload `github-social-preview.png` (1280×640)
2. Organization avatar: Use `avatar-512.png`

## File Formats

### SVG (Vector)
Resolution-independent, preferred for web and modern contexts. Editable in:
- Figma (drag and drop)
- Adobe Illustrator
- Inkscape
- Any modern browser

### PNG (Raster)
Pre-rendered at specific sizes for contexts requiring raster:
- Email clients
- Legacy browsers
- Platform-specific icons (iOS, Android)
- Social media embeds

### ICO (Legacy)
Multi-resolution favicon for IE11 and older browsers. Contains 16×16, 32×32, 48×48.

## Regenerating PNG Assets

The AssetGenerator component can regenerate all PNG assets:

1. Load the app with the AssetGenerator component mounted
2. PNG files will automatically download to your browser
3. Move them to the appropriate `/assets` subdirectories

Alternatively, use a tool like:
- ImageMagick: `magick symbol.svg -resize 512x512 symbol-512.png`
- Inkscape CLI: `inkscape symbol.svg --export-width=512 --export-filename=symbol-512.png`
- realfavicongenerator.net for complete favicon bundle

## Prohibitions

❌ **Do not:**
- Distort, rotate, or skew the symbol
- Change the proportions of the circle or line
- Add effects (shadows, gradients, glows) not in the master
- Place on busy backgrounds that reduce legibility
- Use colors other than specified black/white variants
- Set text in a different typeface
- Separate "phronesis" from "FRAMEWORK" in the lockup

## Support

For questions about asset usage or to report issues:
- GitHub: https://github.com/your-org/phronesis
- Email: hello@phronesis-framework.dev
