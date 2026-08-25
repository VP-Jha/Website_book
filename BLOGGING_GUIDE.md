# Publishing a new mathematics note

The website is framework-free. A new post is an ordinary HTML file, so it remains easy to edit from the `Website` folder.

1. Copy one existing file from the `posts` folder.
2. Rename it using a short lowercase slug, for example `measurable-functions.html`.
3. Update the title, description, canonical URL, heading, date, reading time, table of contents, and article content.
4. Add a matching article card to `blog.html` with `data-topic` and searchable words in `data-search`.
5. Add the new URL to `sitemap.xml` and a new `<item>` to `feed.xml`.
6. Run `npm run check`, then `npm run build`.

## Publish

Upload the project files to the `main` branch of `VP-Jha/Website_book`. In the repository, open **Settings → Pages** once and set **Source** to **GitHub Actions**. The workflow then validates and publishes every push to `main`.
