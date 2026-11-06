---
name: reddit-nav
description: |
  Navigate and interact with Reddit — scroll feed, read posts, view subreddits, search, read comments, and upvote. Use this skill whenever the user mentions Reddit, subreddits, scrolling Reddit, checking Reddit posts, searching Reddit, or interacting with Reddit in any way.
---

# Reddit Navigation Skill

Control the user's Reddit via chrome-devtools-mcp (chromium-devtools tools).

## Prerequisites — Browser must be running

**Before doing anything else, load the `browser-control` skill and follow its instructions to ensure Helium is launched and CDP is accessible on port 9223.**

Quick check:
```bash
curl -s http://127.0.0.1:9223/json/version | head -3
```
If that fails, follow the browser-control skill's launch steps first.

## Layout types and Scrolling

Unlike some platforms with complex split virtual scrollers, Reddit generally uses standard document-level scrolling across its main views.

### 1. Main Feed, Subreddits, and Search Results
- `https://www.reddit.com/`
- `https://www.reddit.com/r/*`
- `https://www.reddit.com/search/*`

These pages rely on infinite scrolling / lazy loading triggered by reaching the bottom of the viewport. The most reliable way to load more content is to simulate keyboard scrolling using CDP:

```js
// Scroll down to load more posts
press_key("PageDown");

// Alternative: If you need to jump multiple pages quickly
press_key("End");
```

### 2. Post / Comments Page
`https://www.reddit.com/r/{subreddit}/comments/{post_id}/*`

Comments are nested directly in the main document. `PageDown` works perfectly to scroll through them.

**Important Note on Lightboxes:** If you click a post from a feed, Reddit often opens it in a modal "lightbox" overlay. While this works, it can make the DOM tree very deep and complex. **For the cleanest view, navigate directly to the post's URL using `navigate_page("url")` instead of clicking the feed link if you intend to perform deep analysis of the comments.**

## Navigation flow

### Open Reddit main feed
```
navigate_page("https://www.reddit.com/")
```

### Open a specific Subreddit
```
navigate_page("https://www.reddit.com/r/{SUBREDDIT_NAME}/")
```

### Search Reddit
Using the search bar directly is usually the most robust method for finding specific topics across all of Reddit:
1. `take_snapshot()`
2. Find the search input textbox (e.g., `textbox "Search Reddit"`)
3. `fill(uid, "your search query")`
4. `press_key("Enter")`

*Search results use a horizontal tab bar to filter by 'All', 'Posts', 'Communities', 'Comments', etc.*

### Open a specific post
You can click a post link from the feed, but if you have the URL, navigating directly is cleaner:
```
navigate_page("https://www.reddit.com/r/.../comments/.../")
```

### Navigating Back
To return to the previous page (e.g., going back to the subreddit feed from a post), use the browser's back navigation:
```
navigate_page(type="back")
```

## Interacting with elements (Upvoting, Clicking)
1. `take_snapshot()` — always get fresh UIDs first
2. `click(uid)` — click the element (e.g., the `button "Upvote"`, a post link, or a "Reply" button)

UIDs change on every page load and after scrolling — always take a fresh snapshot first.

## Known limitations

- Reddit uses infinite scrolling. If you don't see the content you expect, use `press_key("PageDown")` to lazy-load more.
- UIDs are ephemeral — never hardcode them.
- Reddit may occasionally prompt to open in the app or log in (if the session drops). Dismiss these dialogs if they appear.
