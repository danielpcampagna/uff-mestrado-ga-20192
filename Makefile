export-tables:
	cd results; \
		rm -rf tables; \
		./export_tables.sh ../gdpr-prov.db.sqlite

plot:
	#pipenv shell;
	cd results; \
		rm -rf *.pdf *.gv; \
		python3 plot_tables.py $(id)

plot-lastest: export-tables
	$(shell make export-tables | tail -2 | grep -oP '\K\w+-\w+-\w+-\w+-\w+' | xargs -I {} make plot id={})

	# make export-tables | tail -2 | grep -oP '\K\w+-\w+-\w+-\w+-\w+' | xargs -I {} echo "Plot {}"

start-maketing-service:
	npm --prefix ./app-marketing/ install
	npm --prefix ./app-marketing/ start


	
