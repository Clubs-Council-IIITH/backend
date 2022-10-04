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
        instagram
        facebook
        youtube
        twitter
        linkedin
        discord
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
        instagram
        facebook
        youtube
        twitter
        linkedin
        discord
    }
}
"""

CREATE_CLUB_MUTATION = """
mutation createClubMutation($name: String!, $mail: String!, $website: String, $category: String, $state: String, $instagram: String, $facebook: String, $youtube: String, $twitter: String, $linkedin: String, $discord: String) {
    createClub(clubData: {name: $name, mail: $mail, website: $website, category: $category, state: $state,instagram: $instagram, facebook: $facebook, youtube: $youtube, twitter: $twitter, linkedin: $linkedin, discord: $discord}) {
        club {
            id
            name
            mail
            website
            category
            state
            instagram
            facebook
            youtube
            twitter
            linkedin
            discord
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
            CREATE_CLUB_MUTATION, variables={
                "name": "TestClubZero", "mail": "test.club@zero.com"}
        )
        print(response)
        self.assertMatchSnapshot(response)
