# Optima Horizons Consulting: website

The website of Optima Horizons Consulting, AI strategy for every sector.

It is one static page, `index.html`, with its images in `assets/`. There is no build step and no dependency: open `index.html` in a browser, or serve the folder from any static host.

## What is on the page

| Section | Content |
| --- | --- |
| Hero | Proven in Practice. Grounded in Research. Your Strategic Advantage., over a slowly turning sphere of points behind the O |
| Ticker | A moving band of the business areas covered |
| About | The challenge (everyone can buy AI, few turn it into advantage); Bridging Theory & Practice; international experience; three pillars |
| Services | I. Strategic Architecture, II. Operational Guidance, III. Solutions Development |
| Framework | Four questions (Strategy, Data, Technology, Skills) as interactive tabs |
| Focus areas | Eight areas of business operations (strategy, operations, customers, knowledge, risk, finance, people, innovation); each card fills on hover |
| Method | Discover, Design, Deliver, on a timeline that draws itself; then the tailored team: senior consultants, academic scholars and analysts, and AI agents, with transfer to the client at the end |
| Perspectives | Three short points of view that open in place |
| Questions | Five frequent questions that open in place |
| Call to action | Ready to set your horizon? |
| Contact | Email and a form that opens the visitor's email app, addressed to admin@optima-be.com |
| Footer | Navigation, copyright, and a discreet link to the Smart Law Hub |

Every movement stops for visitors whose system asks for reduced motion.

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

- **Netlify** (live): the site deploys from the `optima-horizons` branch and is served at https://optima-advisory.eu. The page's canonical and sharing-preview addresses use that domain; change them in the `<head>` of `index.html` if the domain changes.
- **GitHub Pages**: Settings, Pages, deploy from the `optima-horizons` branch, root folder.
- **Any other host** (Cloud Run, a bucket, a shared host): upload `index.html` and `assets/`.
