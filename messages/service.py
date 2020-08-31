from .models import Message


class MessageService:
    model = Message

    def get_messages(self, order_by='-pub_date', **filters):
        query = self.model.objects

        date_from = filters.get('date_from')
        if date_from:
            query = query.filter(pub_date__gt=date_from)

        user_id = filters.get('user_id')
        if user_id:
            query = query.filter(user_id=user_id)

        query = query.order_by(order_by)
        return query.all()
