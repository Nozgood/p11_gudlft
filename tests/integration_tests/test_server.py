from tests.conftest import client


class TestIndex:
    index_endpoint = '/'

    def test_should_return_index(self, client):
        response = client.get(self.index_endpoint)
        assert response.status_code == 200
        assert "Simply Lift" in response.get_data(as_text=True)


class TestLogout:
    logout_endpoint = '/logout'

    def test_logout_no_follow_redirects(self, client):
        response = client.get(self.logout_endpoint)
        assert response.status_code == 302

    def test_logout_follow_redirects(self, client):
        response = client.get(self.logout_endpoint, follow_redirects=True)
        assert response.status_code == 200
        assert "Simply Lift" in response.get_data(as_text=True)


class TestBook:
    book_endpoint = '/book/Test/Simply%20Lift'

    def test_should_return_welcome_template(self, client):
        response = client.get(self.book_endpoint)
        assert response.status_code == 200
        assert "How many places?" in response.get_data(as_text=True)


class TestShowSummary:
    err_unknown_email = 'Unknown email address'
    show_summary_endpoint = '/showSummary'

    def test_show_summary_unknown_email(self, client):
        response = client.post(self.show_summary_endpoint, data={'email': 'unknown@gmail.com'}, follow_redirects=True)
        assert self.err_unknown_email in response.get_data(as_text=True)
        assert response.status_code == 200
        assert "Simply Lift" in response.get_data(as_text=True)

    def test_show_summary_valid_email(self, client):
        response = client.post(self.show_summary_endpoint, data={"email": "john@simplylift.co"}, follow_redirects=True)
        assert self.err_unknown_email not in response.get_data(as_text=True)
        assert 'Welcome, john@simplylift.co' in response.get_data(as_text=True)
        assert 'Clubs:' in response.get_data(as_text=True)


class TestPurchasePlaces:
    purchase_places_endpoint = '/purchasePlaces'

    def test_purchase_places_competition_not_enough_places(self, client):
        response = client.post(
            self.purchase_places_endpoint,
            data={
                'club': 'Simply Lift',
                'competition': 'Testok',
                'places': '13',
            },
            follow_redirects=True
        )

        assert 'this competition does not have enough places, please reduce your amount' in response.get_data(
            as_text=True)

    def test_purchases_places_club_not_enough_points(self, client):
        response = client.post(
            self.purchase_places_endpoint,
            data={
                'club': 'Iron Temple',
                'competition': 'Testok',
                'places': '10'
            },
            follow_redirects=True
        )

        assert 'your club does not have enough points' in response.get_data(as_text=True)

    def test_purchase_places_more_than_twelve_points(self, client):
        response = client.post(
            self.purchase_places_endpoint,
            data={
                'club': 'Simply Lift',
                'competition': 'Test',
                'places': '13'
            },
            follow_redirects=True
        )

        assert 'you cannot book more than 12 places for your club' in response.get_data(as_text=True)

    def test_purchase_places_past_competition(self, client):
        response = client.post(
            self.purchase_places_endpoint,
            data={
                'club': 'Simply Lift',
                'competition': 'Spring Festival',
                'places': '1'
            },
            follow_redirects=True
        )

        assert "you try to book places for a past competition" in response.get_data(as_text=True)

    def test_purchase_negative_amount_of_places(self, client):
        response = client.post(
            self.purchase_places_endpoint,
            data={
                'club': 'Simply Lift',
                'competition': 'Test',
                'places': '-1'
            },
            follow_redirects=True
        )

        assert "you try to book a negative amount of places" in response.get_data(as_text=True)

    def test_purchases_places_normal_behavior(self, client):
        response = client.post(
            self.purchase_places_endpoint,
            data={
                'club': 'Simply Lift',
                'competition': 'Test',
                'places': '12'
            },
            follow_redirects=True
        )

        assert 'your club does not have enough points' not in response.get_data(as_text=True)
        assert 'Great-booking complete!' in response.get_data(as_text=True)
        assert 'you cannot book more than 12 places for your club' not in response.get_data(as_text=True)
        assert "you try to book places for a past competition" not in response.get_data(as_text=True)
        assert ('this competition does not have enough places, please reduce your amount' not in
                response.get_data(as_text=True))
