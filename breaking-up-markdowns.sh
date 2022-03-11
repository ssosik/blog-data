
function moveit {
    git switch main
    git checkout gitsource_main $1
    git add $1
    git commit -m'move to public'
    git switch gitsource_main
    git rm -r $1
    git commit -m'moved to public'
}
