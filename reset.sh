docker-compose -f docker-compose.prod.yml exec sleeper-legacy-web python manage.py makemigrations
docker-compose -f docker-compose.prod.yml exec sleeper-legacy-web python manage.py migrate --run-syncdb

docker-compose -f docker-compose.prod.yml exec sleeper-legacy-web python manage.py add_league malort
docker-compose -f docker-compose.prod.yml exec sleeper-legacy-web python manage.py add_league chilis

docker-compose -f docker-compose.prod.yml exec sleeper-legacy-web python manage.py add_season 1115109155943047168 --league malort
docker-compose -f docker-compose.prod.yml exec sleeper-legacy-web python manage.py add_season 974904445844684800  --league malort

docker-compose -f docker-compose.prod.yml exec sleeper-legacy-web python manage.py add_season 1115061809024806912 --league chilis
docker-compose -f docker-compose.prod.yml exec sleeper-legacy-web python manage.py add_season 981406894357090304  --league chilis
docker-compose -f docker-compose.prod.yml exec sleeper-legacy-web python manage.py add_season 843243877212196864  --league chilis
docker-compose -f docker-compose.prod.yml exec sleeper-legacy-web python manage.py add_season 721062594185617408  --league chilis
docker-compose -f docker-compose.prod.yml exec sleeper-legacy-web python manage.py add_season 601942076086620160  --league chilis
