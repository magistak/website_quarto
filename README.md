# Medium Blog Integration

This project automatically fetches your Medium posts and generates individual Quarto pages for each post.

## Structure

- `posts/` - Contains individual post files generated from Medium
- `generate-posts.py` - Script that fetches Medium RSS and generates post files
- `update-blog.sh` - Local script to regenerate posts and rebuild site
- `netlify.sh` - Build script for Netlify (includes post generation)

## Usage

### Local Development

To update posts locally:
```bash
./update-blog.sh
```

This will:
1. Fetch latest Medium posts
2. Generate individual `.qmd` files in `posts/` folder
3. Update `index.qmd` with links to all posts
4. Build the site with Quarto

### Netlify Deployment

The site automatically regenerates posts on each Netlify build. The `netlify.sh` script:
1. Installs Quarto
2. Fetches and generates Medium posts
3. Builds the complete site

## Features

- ✅ **Individual URLs**: Each post gets its own URL (`/posts/post-title.html`)
- ✅ **Full content**: Posts display complete content on your site
- ✅ **Medium links**: Easy access to original Medium posts for comments
- ✅ **Auto-generation**: Posts update automatically on build
- ✅ **Clean structure**: Posts organized in dedicated folder
- ✅ **SEO friendly**: Each post has proper metadata and structure

## Configuration

The script currently fetches up to 10 most recent posts. To change this, edit the slice in `generate-posts.py`:
```python
for post in posts[:10]:  # Change 10 to desired number
```
