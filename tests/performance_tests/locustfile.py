from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get('/')

    @task
    def show_summary(self):
        self.client.post(
            '/showSummary',
            {
                'email': 'john@simplylift.co'
            }
        )

    @task
    def purchase_places(self):
        self.client.post(
            '/purchasePlaces',
            {
                "club": "Simply Lift",
                "competition": "Testok",
                "places": "1"
            }
        )

    @task
    def book(self):
        self.client.get('/book/Testok/Simply%20Lift')

    @task
    def logout(self):
        self.client.get('/logout')
