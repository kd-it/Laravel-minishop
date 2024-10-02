all: testall

LOCKFILE=/tmp/up.run
PULL=missing
# Laravel環境を使わない場合は実行時にNO_LARAVEL=を指定してください
NO_LARAVEL=

# composer.json(lock)からvendorディレクトリを作成します
vendor: composer.json
	@if [ -z "$(NO_LARAVEL)" ]; then \
		composer install; \
		touch vendor; \
	else \
		echo "[INFO] NO_LARAVELが宣言されているのでcomposer installをスキップします。"; \
	fi

# artisanによりLaravel環境のデータベースの初期化をしなおします
resetenv:
	@if [ -z "$(NO_LARAVEL)" ]; then \
		php artisan migrate:fresh --seed; \
	else \
		echo "[INFO] NO_LARAVELが宣言されているのでデータベース初期化処理をスキップします。"; \
	fi

# テストを実行します(tests/*.py)
testall: python-init
	for i in tests/*.py; do \
		make resetenv; \
		pipenv run python $$i; \
	done

# 個別にテストを実行します
test: python-init resetenv
	pipenv run python $(FILE)

up: $(LOCKFILE)

down:
	docker compose -p test down --rmi local -t 3 -v
	make clean

$(LOCKFILE):
	docker compose -p test -f compose.yml -f compose_test.yml up --pull $(PULL) --quiet-pull -d | tee $(LOCKFILE)
	sleep 5
	@echo "Waiting for db to be ready..."
	sh -c "while ! docker exec --env-file=./env.txt $$(docker compose -p test ps -q db) /usr/local/bin/healthcheck.sh; do sleep 1; done"
	touch $(LOCKFILE)

clean: down
	rm -f $(LOCKFILE)


testall_in_docker: up
	docker compose -p test exec -w /app app make testall NO_LARAVEL=$(NO_LARAVEL)
	make down

test_in_docker: up
	docker compose -p test exec -w /app app make test FILE=$(FILE) NO_LARAVEL=$(NO_LARAVEL)
	make down


python-init:
	if ! which pipenv; then pip install pipenv --break-system-packages; fi
	pipenv install --dev

