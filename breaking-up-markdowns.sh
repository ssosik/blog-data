function moveit {
    if [ -z $1 ] ; then
        echo need a file
    else
        git switch new
        git checkout old $1
        git add $1
        git commit -m"move $1 to public"
        git switch old
        git rm -r $1
        git commit -m"moved $1 to public"
        git switch new
    fi
}
