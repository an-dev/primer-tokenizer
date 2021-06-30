# Primer-Token

Quick task implementation


## Installation
- To install, clone the repository locally: `git clone `
- Create virtualenv: `python3 -m venv .venv`
- Activate virtualenv: `source .venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Migrate and load data from dump `python manage.py migrate && python manage.py loaddata dump.json`


## Testing
Test via django built in command: `python manage.py test`

## Usage

### create restaurants with a restaurant name
```
curl --request POST \
  --url http://localhost:8000/api/restaurants/ \
  --header 'Content-Type: application/json' \
  --cookie csrftoken=ie7XqnpyEKTHkY6ldoQMncBf6bK7J66m2HfHovNJX3L7ZUCbQiH9w7WT0mtpE80R \
  --data '{
	"name": "Bestest Fish n Chips"
    }'
```

### view all restaurants with pagination
```
curl --request GET \
  --url http://localhost:8000/api/restaurants/ \
  --header 'Content-Type: application/json' \
  --cookie csrftoken=ie7XqnpyEKTHkY6ldoQMncBf6bK7J66m2HfHovNJX3L7ZUCbQiH9w7WT0mtpE80R
```

### add a name & email address to a waitlist for a specific restaurant
```
curl --request POST \
  --url http://localhost:8000/api/restaurants/2/waitlist/ \
  --header 'Content-Type: application/json' \
  --cookie csrftoken=ie7XqnpyEKTHkY6ldoQMncBf6bK7J66m2HfHovNJX3L7ZUCbQiH9w7WT0mtpE80R \
  --data '{
	"name":"Andy",
	"email":"yeahthebest92@hotmail.it"
    }'
```

### remove an entry for a specific email address from a waitlist for a specific restaurant
```
curl --request POST \
  --url http://localhost:8000/api/restaurants/2/waitlist/entry/ \
  --header 'Content-Type: application/json' \
  --cookie csrftoken=ie7XqnpyEKTHkY6ldoQMncBf6bK7J66m2HfHovNJX3L7ZUCbQiH9w7WT0mtpE80R \
  --data '{
	"email":"yeahthebest92@hotmail.it"
    }'
```

### view a waitlist for a restaurant
```
curl --request GET \
  --url http://localhost:8000/api/restaurants/2/waitlist/ \
  --header 'Content-Type: application/json' \
  --cookie csrftoken=ie7XqnpyEKTHkY6ldoQMncBf6bK7J66m2HfHovNJX3L7ZUCbQiH9w7WT0mtpE80R

```

## Notes
TODO



## References
Web pages used/consulted while building the script

https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset

https://www.django-rest-framework.org/api-guide/testing/#testing
