
# verwijderen ~ bestanden
find ./ -name "*~"    -ls -delete
find ./ -name "*.pyc" -ls -delete

git add *.html
git add *.sql
git add *.py
git add .gitignore
git add *.sh
git add *.jpg
git add *.css
git add *.txt
git add README

git status
