# Optima Horizons Consulting: website

The website of Optima Horizons Consulting, AI strategy for every sector.

It is one static page, `index.html`, with its images in `assets/`. There is no build step and no dependency: open `index.html` in a browser, or serve the folder from any static host.

## What is on the page

| Section | Content |
| --- | --- |
| Hero | Scholarly Insight. Strategic Advantage. |
| About | Bridging Theory & Practice; Research Backed, Every Sector, Excellence Driven |
| Services | I. Strategic Architecture, II. Operational Guidance, III. Solutions Development |
| Framework | Strategy, Data, Technology, Skills: from today to what must change |
| Sectors | Eight industries, from legal and financial services to the public sector |
| Method | Three phases, the AI leverage measure, what a released hour is worth |
| Contact | Email and a form that opens the visitor's email app, addressed to admin@optima-be.com |
| Footer | Navigation, copyright, and a discreet link to the Smart Law Hub |

## Brand

Colours, fonts and logo follow the Optima Horizons visual identity.

| Token | Hex | Use |
| --- | --- | --- |
| Ink | `#1E2E33` | Dark sections, titles |
| Slate | `#3F5C66` | Panels, accents |
| Mist | `#6F8C96` | The muted O, secondary text on dark |
| Line | `#D5E0E4` | Rules, borders |
| Paper | `#EDF2F3` | Light panels |

Titles use Cambria (Caladea from Google Fonts where Cambria is missing). Labels use Montserrat in spaced capitals. Body text uses Helvetica or Arial.

`assets/` holds the white logo, the slate logo, the white O mark, the favicons and a 1200×630 social sharing card.

## Editing

- **Contact email**: change `CONTACT_EMAIL` near the end of `index.html`. The page shows and uses that address everywhere.
- **Text**: every section is plain HTML in `index.html`, marked with a comment (`<!-- Services -->` and so on).
- **Colours**: the tokens at the top of the `<style>` block.

## Publishing

- **Netlify**: import the repository, pick the `optima-horizons` branch; `netlify.toml` publishes the root folder.
- **GitHub Pages**: Settings, Pages, deploy from the `optima-horizons` branch, root folder.
- **Any other host** (Cloud Run, a bucket, a shared host): upload `index.html` and `assets/`.
