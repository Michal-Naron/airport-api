# Airport-API 
> A REST API for managing airports, flights, crews, airplanes, and tickets built with Django REST Framework.

## Check it out!
[Airport API deployed](#) *(replace with your deployed link if available)*

For demonstration purposes, two user accounts have been created so you can explore the API from different perspectives:

- **michał**
  - Username: michal
  - Password: 123456
  - This account allows you to create orders and view your tickets.

- **jan**
  - Username: jan
  - Password: 123456
  - This account allows you to explore admin-level operations if staff privileges are enabled.

> To log in, visit: `/api/v1/user/login/`


## Run with docker
```
docker-compose build
docker-compose up -d
```
## Features


* Authentication system for users
* Airports, Routes, Airplanes & Crews management
* Flight creation with route, airplane, and crew assignment
* Ticket ordering and management system
* Order history for users
* Admin-only operations for managing airplanes, flights, and tickets
* Image upload support for airplanes
* Filtering & searching flights by route, departure, or arrival dates
* Powerful REST API with proper permissions for admin vs regular users
* Clean, structured API endpoints for all resources

## API Documentation

The full API documentation with all endpoints, request/response examples, and models is available via Swagger UI at:
http://localhost:8000/swagger/