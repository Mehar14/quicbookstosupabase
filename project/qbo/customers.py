from quickbooks.objects.customer import Customer

def fetch_customers(qbo_client):
    return Customer.all(qb=qbo_client)