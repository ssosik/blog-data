
git switch main
git checkout gitsource_main $ITEM
git add $ITEM
git commit -m'move to public'
git switch gitsource_main
git rm -r $ITEM
git commit -m'moved to public'
