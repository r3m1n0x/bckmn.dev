# bckmn.dev

Marvin Beckmann's personal website and infrastructure blog. English content,
Gruvbox-inspired shell styling, project-owned Hugo templates, and GitHub Pages.
No theme, Node, Go modules, external fonts, or JavaScript are required.

## Start locally

The project pins Hugo in `.hugo-version` (currently **0.166.0**). The wrapper uses
`.tools/hugo` first and otherwise accepts a matching Hugo from your PATH. It does
not replace a system-wide or Go-installed Hugo.

```sh
./scripts/install-hugo
./scripts/hugo server --buildDrafts --disableFastRender --noHTTPCache
```

Open http://localhost:1313. The installer supports Linux amd64/arm64 and macOS,
downloads the official release, and verifies its SHA-256 checksum. WSL uses the
Linux installer. Python 3 is needed only for the verification script.

Omit `--buildDrafts` to see the publication state. The short introductory post is
ready for release. The DNS layout specimen remains a labeled, unpublished draft.

## Write

```sh
./scripts/hugo new content blog/my-first-note/index.md
```

Edit the Markdown page bundle under `content/blog/`, placing images beside the
article. Required metadata: title, description, date, and draft status. Optional:
`format` (Note, Article, Lab note), `tags`, and `toc`. Use a date with a timezone.
Set `draft: false` only when the content is ready. Dates sort newest first; the
homepage shows five posts and the archive paginates after ten.

Do not copy `preview: true` from the specimen into a real article. Preview
specimens never appear in RSS, and the production check rejects the current
specimen if it is accidentally published.

## Build and verify

Use separate destinations when switching between draft and production builds.
Hugo does not automatically remove output left over from an earlier draft build.

```sh
./scripts/hugo --destination /tmp/bckmn-release --minify --panicOnWarning
python3 scripts/check-site.py /tmp/bckmn-release
```

For a draft build, pass `--buildDrafts` to Hugo and `--preview` to the checker.
Use a fresh output directory for a release. Generated `public/`, `resources/`,
and downloaded `.tools/` are ignored and must not be committed.

## Structure

- `hugo.yaml`: canonical domain, locale, markup, pagination.
- `content/`: About, blog page bundles, and imprint with privacy information.
- `layouts/`: HTML templates, breadcrumbs, blog-only RSS, robots.txt.
- `assets/css/site.css`: shared responsive design, fingerprinted by Hugo.
- `static/`: favicon and GitHub Pages CNAME.
- `scripts/`: pinned Hugo launcher/installer and generated-site checks.

## Deployment and maintenance

The workflow verifies pull requests. On pushes to `main` or a manual run on
`main`, a separate deployment job builds and checks again, then publishes to the
existing **gh-pages** branch. Only that job has repository write permissions.
The existing Pages branch configuration is retained; no remote setting was
changed as part of the redesign. Confirm Pages uses `gh-pages` at `/` before the
first release. The canonical domain and `static/CNAME` are `www.bckmn.dev`.

Hugo uses the same `.hugo-version` locally and in CI. To upgrade, edit that file,
rerun the installer, and build/check both publication states. Dependabot checks
GitHub Actions weekly. Extended Hugo is unnecessary for the current CSS-only site.

There is no automatic Medium cross-posting. The personal domain remains the
original publication location.

About and the introductory article use the owner's briefing. The imprint uses
the updated address and the contact email already present in the previous site
configuration. Privacy information describes the current static site and GitHub
Pages. Update it whenever hosting,
tracking, embedded content, or contact handling changes. It has not had a lawyer's
review. Employment dates, CV details, and certifications have not been fabricated.
