from marshmallow import Schema, fields

class UserSchema(Schema):
    class Meta:
        fields = ('id', 'username', 'role', 'is_admin', 'approved', 'active')

class VenueSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'place', 'capacity')

class ShowSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'rating', 'tags', 'image_path', 'ticket_price', 'venue_id')

class BookingSchema(Schema):
    class Meta:
        fields = ('id', 'quantity', 'show_id', 'user_id', 'venue_id')

# Add more schemas for other models if needed
