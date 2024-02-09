from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get('/')

    @task
    def refresh_page(self):
        self.client.post(
            '/purchasePlaces',
            {
                "club": "Simply Lift",
                "competition": "Testok",
                "places": "2"
            }
        )
