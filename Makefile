xml_to_csv:
	docker build -f app/Dockerfile_app ./app -t xml_to_csv --target xml_to_csv
	docker run -it xml_to_csv

run:
	docker stop app_test_c1 || true
	docker rm app_test_c1 || true
	docker rmi app_test || true

	docker stop truelayer_db_c1 || true
	docker rm truelayer_db_c1 || true
	docker rmi truelayer_db || true

	docker stop app_prod || true
	docker rm app_prod || true
	docker rmi app_prod || true

	docker-compose build
	docker-compose --compatibility up
	sleep 5

test:
	docker stop app_test_c1 || true
	docker rm app_test_c1 || true
	docker rmi app_test || true
	docker build -f app/Dockerfile_app ./app -t app_test --target test
	docker run -it app_test



.PHONY: run, test, xml_to_csv
