#!/bin/bash

echo "🔄 Fetching latest Medium posts and generating pages..."

# Remove old generated post files (keep originals)
rm -f posts/post-*.qmd
rm -f index-generated.qmd

# Generate new posts
python3 generate-posts.py

if [ $? -eq 0 ]; then
    echo "✅ Posts generated successfully!"
    
    # Backup current index if it exists
    if [ -f "index.qmd" ]; then
        cp index.qmd index-backup.qmd
        echo "📦 Backed up current index.qmd to index-backup.qmd"
    fi
    
    # Replace index with generated version
    cp index-generated.qmd index.qmd
    echo "🔄 Updated index.qmd with latest posts"
    
    # Render the site
    echo "🏗️  Building site..."
    quarto render
    
    if [ $? -eq 0 ]; then
        echo "🎉 Site built successfully!"
        echo "🌐 Your blog is ready with individual post pages!"
    else
        echo "❌ Build failed"
        exit 1
    fi
else
    echo "❌ Failed to generate posts"
    exit 1
fi
