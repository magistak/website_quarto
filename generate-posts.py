#!/usr/bin/env python3

import urllib.request
import json
import re
import os
from html import unescape

def fetch_medium_feed():
    """Fetch Medium RSS feed via rss2json API"""
    url = 'https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/@magistak'
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"Error fetching feed: {e}")
        return None

def create_slug(title):
    """Create a URL-friendly slug from title"""
    # Remove HTML tags and decode entities
    title = re.sub(r'<[^>]+>', '', title)
    title = unescape(title)
    
    # Convert to lowercase and replace non-alphanumeric with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower())
    slug = re.sub(r'^-+|-+$', '', slug)
    
    # Limit length
    return slug[:50]

def clean_content(html):
    """Clean HTML content for Quarto"""
    if not html:
        return ""
    
    # Remove script and style tags
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove style attributes
    html = re.sub(r'style="[^"]*"', '', html, flags=re.IGNORECASE)
    
    # Fix image sizing for mobile - make all images responsive
    html = re.sub(r'<img([^>]*?)>', r'<img\1 style="max-width: 100%; height: auto;">', html, flags=re.IGNORECASE)
    
    # Also handle figure tags
    html = re.sub(r'<figure([^>]*?)>', r'<figure\1 style="max-width: 100%; text-align: center;">', html, flags=re.IGNORECASE)
    
    # Decode HTML entities
    html = unescape(html)
    
    return html

def generate_post_file(post):
    """Generate Quarto file for a single post"""
    slug = create_slug(post['title'])
    filename = f"posts/post-{slug}.qmd"
    
    # Skip if file already exists (for faster builds)
    if os.path.exists(filename):
        print(f"Skipped (exists): {filename}")
        # Still return the post info for index generation
        from datetime import datetime
        try:
            date_obj = datetime.strptime(post['pubDate'], '%Y-%m-%d %H:%M:%S')
            formatted_date = date_obj.strftime('%Y-%m-%d')
        except:
            formatted_date = post['pubDate'][:10]  # fallback
        
        return {
            'title': post['title'],
            'slug': slug,
            'filename': filename,
            'date': formatted_date,
            'link': post['link'],
            'description': re.sub(r'<[^>]+>', '', post.get('description', ''))[:150] + '...'
        }
    
    # Skip if file already exists
    if os.path.exists(filename):
        print(f"Skipped (exists): {filename}")
        # Still return the post info for index generation
        from datetime import datetime
        try:
            date_obj = datetime.strptime(post['pubDate'], '%Y-%m-%d %H:%M:%S')
            formatted_date = date_obj.strftime('%Y-%m-%d')
        except:
            formatted_date = post['pubDate'][:10]
        
        return {
            'title': post['title'],
            'slug': slug,
            'filename': filename,
            'date': formatted_date,
            'link': post['link'],
            'description': re.sub(r'<[^>]+>', '', post.get('description', ''))[:150] + '...'
        }
    
    # Format date
    from datetime import datetime
    try:
        date_obj = datetime.strptime(post['pubDate'], '%Y-%m-%d %H:%M:%S')
        formatted_date = date_obj.strftime('%Y-%m-%d')
    except:
        formatted_date = post['pubDate'][:10]  # fallback
    
    # Escape title for YAML
    title_escaped = post['title'].replace('"', '\\"')
    
    # Get content
    content = clean_content(post.get('content', post.get('description', '')))
    
    # Generate file content
    file_content = f'''---
title: "{title_escaped}"
date: "{formatted_date}"
format: html
---

::: {{.callout-note appearance="simple"}}
This post was originally published on [Medium]({post['link']}). You can also read it there and leave comments.
:::

{content}

---

::: {{.text-center}}
[**Read and Comment on Medium**]({post['link']}){{.btn .btn-primary .btn-lg target="_blank"}}
:::
'''

    # Write file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(file_content)
    
    print(f"Generated: {filename}")
    
    return {
        'title': post['title'],
        'slug': slug,
        'filename': filename,
        'date': formatted_date,
        'link': post['link'],
        'description': re.sub(r'<[^>]+>', '', post.get('description', ''))[:150] + '...'
    }

def generate_index_file(posts):
    """Generate updated index.qmd with links to individual posts"""
    
    posts_list = []
    for post in posts:
        posts_list.append(f"- [**{post['title']}**](posts/post-{post['slug']}.html) - *{post['date']}*  \n  {post['description']}")
    
    posts_content = '\n\n'.join(posts_list)
    
    index_content = f'''---
title: "My blog from Medium"
format: html
---

To view all posts on Medium, visit [medium.com/@magistak](https://medium.com/@magistak).

📚 [**Browse all posts**](posts/) organized with search and filtering.

## Recent Posts

{posts_content}

---

*All posts are also available on [Medium](https://medium.com/@magistak) where you can leave comments and engage with the community.*
'''

    with open('index-generated.qmd', 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print('Generated: index-generated.qmd')

def main():
    print('Fetching Medium posts...')
    
    data = fetch_medium_feed()
    if not data or data.get('status') != 'ok':
        print('Failed to fetch Medium feed')
        return
    
    posts = data.get('items', [])
    print(f'Found {len(posts)} posts')
    
    # Create posts directory if it doesn't exist
    import os
    os.makedirs('posts', exist_ok=True)
    
    # Generate individual post files (limit to 10 most recent)
    generated_posts = []
    for post in posts[:10]:
        try:
            generated_post = generate_post_file(post)
            generated_posts.append(generated_post)
        except Exception as e:
            print(f"Error generating post '{post.get('title', 'Unknown')}': {e}")
    
    # Generate index file
    if generated_posts:
        generate_index_file(generated_posts)
        print(f'\nAll files generated successfully!')
        print('Run "quarto render" to build the site')
    else:
        print('No posts were generated')

if __name__ == '__main__':
    main()
