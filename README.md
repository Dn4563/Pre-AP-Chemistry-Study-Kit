# Pre-AP Chemistry Study Kit by David Noskow

Live site: https://dn4563.github.io/Pre-AP-Chemistry-Study-Kit/

The page opens on a list of chapters. Each chapter has Learn, Study guide, Cheat sheet, Flashcards, Quiz, Practice Test, Full exam, Progress and Settings. Progress saves in the browser, separately for each chapter.

`index.html` is **built**. Don't edit it by hand: edit the files in `content/`, then build.

## Folders

| Path | What it is |
|---|---|
| `content/course.json` | Course name, colors, Study Hub link, and the list of chapters |
| `content/ch03-matter/` | Everything in Chapter 3 (one folder per chapter) |
| `core/` | Copy of the shared engine from the Study Hub repo. Don't edit it here; see "Update the engine" below. |
| `scripts/` | `parse.mjs` (content to `data.json`), `build.mjs` (builds `index.html`), `sync-core.mjs` |
| `test/` | The click-through test |
| `legacy/index.html` | The old hand-made page, kept as a backup |

## Inside a chapter folder

| File | What goes in it |
|---|---|
| `cards.md` | Every term. `# Deck 1: Name`, then `## Section name`, then table rows `\| Term \| Definition \| Hook \|`. Leave Hook blank if there isn't one. Add `(optional)` to the end of a deck heading to keep that deck out of All decks unless it's turned on in Settings. |
| `watch.md` | Watch-out notes, one per line: `- (deck 2) text`. Use these where the slides, review sheet or textbook disagree. |
| `trees.md` | Text trees for hierarchies, each in a fenced code block |
| `guide.json` | Flow chains (`flows`), comparison tables (`tables`), the cheat sheet (`cheat`), and `topicDeck`, which says which deck to review for each practice topic |
| `scenarios.json` | Scenario questions used in Learn checkpoints and the Quiz |
| `practice.json` | Practice Test and Full exam sections and questions. Question formats are listed in `core/README.md`. |
| `images.json`, `assets/` | Images used by diagram questions |

Question-writing rules:
- Keep option lengths similar; the right answer is never the longest option.
- Balance which letter is correct.
- Give every wrong option a `why`, and never refer to a choice by letter (choices get shuffled).

## Add a chapter

1. Make a folder, for example `content/ch04-atoms/`, with the files above. Copy `ch03-matter` to start.
2. Add the chapter to `units` in `content/course.json`:
   ```json
   { "id": "ch04", "dir": "ch04-atoms", "label": "Chapter 4", "title": "Atoms", "blurb": "One sentence on what it covers." }
   ```
3. Build and test (below).
4. Add the chapter to this course's `units` in the Study Hub's `courses.json`.

## Add a diagram-labeling question

1. Find an **unlabeled** image on Wikimedia Commons or OpenStax, and check that its license allows reuse. Save it in `assets/` and add it to `images.json`: `"distill": "assets/distillation-unlabeled.png"`.
2. In `practice.json`, add a question with `"type": "diagram"`. Give it:
   - `img` (the key from `images.json`)
   - `alt` (a description of the image)
   - `credit` (required; shown under the image)
   - `labels` (the answer choices)
   - `pins`: each pin has `x` and `y` (percent across and down the image), `ans` (the index of the right label) and `exp` (a short explanation)
3. Build. The build stops with a message if the image or credit is missing or a pin is off the image.

## Build and test

You need Node 18 or newer. The first time, run:

```bash
npm install
```

Then, after every change:

```bash
npm test
```

`npm test` parses the content, builds `index.html`, and clicks through every tab in a simulated browser. It runs a lesson, a quiz, flashcards, every practice section, a diagram, exam results, save and reload, export, import and reset. It prints `PASS`, or `FAIL` with the reason. Use `npm run build` to build without testing.

To look at the page, open `index.html` in a browser. Add `#ch03` to the address to jump straight to Chapter 3.

## Update the engine

The engine lives in the Study Hub repo (`Study-Hub-by-David/kit-core`). Clone both repos into the same folder, then run:

```bash
npm run sync-core
```

```bash
npm test
```

## Publish on GitHub Pages

1. Commit `index.html` together with your content changes, and merge into `main`.
2. Pages is already on (Settings → Pages, branch `main`, folder `/ (root)`). The site updates about a minute after the merge.
