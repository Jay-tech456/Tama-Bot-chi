# Running the Sanity Studio locally

This folder hosts the Sanity Studio for Socios. Follow the steps below to get it running locally.

## Prerequisites

1. **Node.js 18+** (check with `node -v`).
2. **npm 9+** (bundled with Node).
3. Access to the Sanity project `c0j8rp13` using the `production` dataset (configured in `sanity.config.ts`).

## Install dependencies

```bash
npm install
```

> Run the command from this `studio-sanity` directory so the correct `package.json` is used.

## Start the Studio locally

```bash
npm run dev
```

This starts `sanity dev` on <http://localhost:3333>. The CLI will prompt you to log in to Sanity if needed.

## Useful scripts

- `npm run start` – run `sanity start` (legacy alias for `dev`).
- `npm run build` – build the Studio for production.
- `npm run deploy` – deploy the Studio to Sanity-hosted infrastructure.

That’s it—once `npm run dev` is up, you can begin editing content locally. Let me know if you need environment variable guidance or custom dataset instructions.
