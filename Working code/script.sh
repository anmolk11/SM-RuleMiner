for i in {1..5}; do
	python main.py
done
git add log_testing.xlsx
git add log_rules.xlsx
git commit -m "Log updated"
git push