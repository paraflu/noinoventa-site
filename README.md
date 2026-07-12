# Associazione NOI — Sito Istituzionale

Sito web dell'Associazione NOI di Noventa di Piave, costruito con [Astro](https://astro.build) e pubblicato su [Cloudflare Pages](https://pages.cloudflare.com).

## Stack

- **Framework**: Astro (static site generator)
- **Stile**: Tailwind CSS
- **Deploy**: Cloudflare Pages via GitHub Actions

## Sviluppo

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # build statico in dist/
npm run preview    # preview del build
```

## Struttura

```
src/
├── layouts/
│   ├── Layout.astro        # Layout base (HTML shell)
│   └── BaseLayout.astro    # Layout con Header + Footer
├── components/
│   ├── Header.astro        # Navigazione
│   └── Footer.astro        # Pie di pagina
├── pages/
│   ├── index.astro         # Home
│   ├── dove-siamo.astro    # Contatti e mappa
│   ├── notizie/index.astro # News
│   └── galleria/index.astro # Galleria fotografica
└── styles/
    └── global.css          # Tailwind imports
```

## Deploy

Il deploy avviene automaticamente tramite GitHub Actions ad ogni push su `main`.

## License

MIT
