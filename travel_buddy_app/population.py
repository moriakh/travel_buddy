from travel_buddy_app.models import Users, Trips

adan = Users.objects.create(name = 'Adan', username = 'firstman', email = 'adan@testing.com', password = '12345678')
eve = Users.objects.create(name = 'eve', username = 'firstwhat?', email = 'eve@testing.com', password = '12345678')
eden = Trips.objects.create(destination = 'Eden', start_date = '2021-09-13', end_date = '2021-09-21', plan = 'Eat some apples')
eve.trips.add(eden)
eve.own_trips.add(eden)
adan.trips.add(eden)