git add .;
read -p "Commit Name : " commit_name
git commit -m "$commit_name"
git push -u origin main;
echo "Commit successful"