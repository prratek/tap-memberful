"""Memberful tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_memberful.streams import (
    MemberfulStream,
    ActivitiesStream,
    MembersStream,
    OrdersStream,
    PlansStream,
    SubscriptionsStream,
)


STREAM_TYPES = [
    ActivitiesStream,
    MembersStream,
    OrdersStream,
    PlansStream,
    SubscriptionsStream,
]


class TapMemberful(Tap):
    """Memberful tap class."""
    name = "tap-memberful"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            description="The token to authenticate against the API service"
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
