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
- `content/`: About, CV, blog page bundles, and imprint with privacy information.
- `data/certifications.yaml`: certification names and official information links.
- `layouts/`: HTML templates, breadcrumbs, blog-only RSS, robots.txt.
- `layouts/cv/single.html`: CV header, contact details, and section navigation.
- `assets/css/site.css`: shared responsive design, fingerprinted by Hugo.
- `static/`: favicon and GitHub Pages CNAME.
- `static/images/certifications/`: locally served, unmodified CNCF certification logos.
- `scripts/`: pinned Hugo launcher/installer and generated-site checks.

## Photography

The gallery at `/gallery/` is published with the first selected photograph.
Links appear automatically on About and in the main navigation when the gallery
is included in the build and has photos. Use `draft: true` to hide it from
publication and `--buildDrafts` to review drafts locally.
Add selected photos to `assets/photography/`, then list them in the `photos`
front matter of `content/gallery/index.md` in the desired display order:

```yaml
photos:
  - file: example.jpg
    title: A short title
    alt: A description of what the photograph shows
    caption: Optional context for the photograph
```

Hugo creates responsive WebP previews and a JPEG view up to 2400 pixels, preserving
the composition and applying EXIF orientation. Only the processed images are
published; source files in `assets/` are not copied to the site. Processing strips
image metadata. The source files themselves are still part of the repository, so
use photos prepared for sharing. Supported inputs include JPEG, PNG, and WebP.

Click a photo to enlarge it. The native HTML popover closes with its Close button,
Escape, or a click outside; an ordinary image link is also available. No JavaScript
or external image service is required. With an empty photo list, the gallery shows
a short notice. The image-processing behavior follows the
[Hugo documentation](https://gohugo.io/content-management/image-processing/).

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

The CV has a dedicated print stylesheet. Use the browser's Print menu and choose
"Save as PDF" to export the current page; navigation and screen-only instructions
are omitted. CV roles live in Markdown using the `cv-role` shortcode; certification
names are shared with About through `data/certifications.yaml`.

About and CV use the owner's briefing, CV, and corrections. The CV is available
at `/cv/`, with `/resume/` redirecting there. The owner confirmed that plusserver
remains the current employer; the end date in the attached reference is incorrect.
The current role is Senior DevOps-Engineer Kubernetes, as confirmed by the owner.
Propagator is presented as ongoing development, based on the owner's description
and its repository README. The repository is currently private, so the public
pages describe the project without a repository link or claims of production use.
The introductory article uses the briefing. The imprint uses
the updated address and the contact email already present in the previous site
configuration. Privacy information describes the current static site and GitHub
Pages. Update it whenever hosting,
tracking, embedded content, or contact handling changes. It has not had a lawyer's
review. Employment dates, CV details, and certifications have not been fabricated.
The owner confirmed CKS, CKA, and CKAD; the certification links lead to programme
information, not personal credential verification. No issue or expiry dates are
asserted. Logo sources are documented in `CERTIFICATION-ARTWORK.md`.
