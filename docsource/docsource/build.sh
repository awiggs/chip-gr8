# Rename docs
mv docs out

# Build
npm run build

# Export 
npm run export

# Rename out
mv out docs

# Add nojekyll
touch docs/.nojekyll