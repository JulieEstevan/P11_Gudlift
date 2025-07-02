from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    club = "Simply Lift"
    competition = "Summer Showdown"

    def on_start(self):
        self.client.post("/show_summary", data={"email": "john@simplylift.co"})
        self.club_name = self.club
        self.competition_name = self.competition

    @task(4)
    def load_index_page(self):
        self.client.get("/", name="Index Page")

    @task(3)
    def load_summary_page(self):
        with self.client.post("/show_summary", data={"email": "john@simplylift.co"}, catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure("Response took too long")
            else:
                response.success()

    @task(2)
    def load_bookings_page(self):
        self.client.get(f"/book/{self.competition}/{self.club}", name="Booking Page")

    @task(1)
    def load_points_page(self):
        with self.client.get("/clubs_points", name="Clubs Points Page", catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Response took too long")
            else:
                response.success()

    @task(1)
    def purchase_places(self):
        data = {
            "competition": self.competition,
            "club": self.club,
            "places": 2  # Example number of places
        }
        with self.client.post("/purchase_places", data=data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Failed to purchase places")
