from snapshottest import TestCase
from graphene.test import Client
from mixer.backend.django import mixer
from club_manager.schema import schema
from club_manager.models import Club

ALL_CLUBS_QUERY = """
{
    clubs {
        img
        name
        mail
        website
        category
        state
        tagline
        description
    }
}
"""

SPECIFIC_CLUB_QUERY = """
{
    club(clubId: $id) {
        img
        name
        mail
        website
        category
        state
        tagline
        description
    }
}
"""

CREATE_CLUB_MUTATION = """
mutation createClubMutation($name: String!, $mail: String!, $website: String, $category: String, $state: String) {
    createClub(clubData: {name: $name, mail: $mail, website: $website, category: $category, state: $state}) {
        club {
            id
            name
            mail
            website
            category
            state
        }
    }
}
"""


class ClubSnapshotCase(TestCase):
    def setUp(self):
        self.client = Client(schema)
        self.club0 = mixer.blend(Club)
        self.club1 = mixer.blend(Club)
        return super().setUp()

    def test_query_all_clubs(self):
        response = self.client.execute(ALL_CLUBS_QUERY)
        self.assertMatchSnapshot(response)

    def test_query_specific_club(self):
        response = self.client.execute(
            SPECIFIC_CLUB_QUERY, variables={"id": getattr(self.club1, "id", 0)}
        )
        self.assertMatchSnapshot(response)

    def test_mutation_create_club(self):
        response = self.client.execute(
            CREATE_CLUB_MUTATION, variables={"name": "TestClubZero", "mail": "test.club@zero.com"}
        )
        print(response)
        self.assertMatchSnapshot(response)
