for i in {1..10}; do
	python main.py
done
git add log.xlsx
git add rules_log.txt
git commit -m "Log updated"
git push