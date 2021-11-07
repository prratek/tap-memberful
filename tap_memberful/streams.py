"""Stream type classes for tap-memberful."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_memberful.client import MemberfulStream


class ActivitiesStream(MemberfulStream):
    """Define custom stream."""
    name = "activities"
    primary_keys = ["id"]
    replication_key = "createdAt"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("createdAt", th.IntegerType),
        th.Property("type", th.StringType),
        th.Property(
            "member",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("stripeCustomerId", th.StringType),
                th.Property("email", th.StringType),
            )
        ),
    ).to_dict()

    query = """
        query ($afterCursor: String!) {
            activities(after: $afterCursor) {
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                }
                edges {
                    node {
                    createdAt
                        id
                        member {
                            id
                        }
                        type
                    }
                }
            }
        }
        """


class MembersStream(MemberfulStream):
    """Define custom stream."""
    name = "members"
    primary_keys = ["id"]

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("email", th.StringType),
        th.Property(
            "address",
            th.ObjectType(
                th.Property("city", th.StringType),
                th.Property("country", th.StringType),
                th.Property("postalCode", th.StringType),
                th.Property("state", th.StringType),
                th.Property("street", th.StringType),
            )
        ),
        th.Property(
            "creditCard",
            th.ObjectType(
                th.Property("brand", th.StringType),
                th.Property("expMonth", th.IntegerType),
                th.Property("expYear", th.IntegerType),
                th.Property("lastFourDigits", th.StringType),
            )
        ),
        th.Property("customField", th.StringType),
        th.Property("discordUserId", th.StringType),
        th.Property("fullName", th.StringType),
        # th.Property("metadata", th.StringType),  TODO: Stringify?
        th.Property("phoneNumber", th.StringType),
        th.Property("stripeCustomerId", th.StringType),
        th.Property("totalOrders", th.IntegerType),
        th.Property("totalSpendCents", th.IntegerType),
        # th.Property("trackingParams", th.StringType),  TODO: Stringify?
        th.Property("unrestrictedAccess", th.BooleanType),
        th.Property("username", th.StringType),
    ).to_dict()

    query = """
        query ($afterCursor: String!) {
            members(after: $afterCursor) {
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                }
                edges {
                    node {
                        id
                        email
                        address {
                            city
                            country
                            postalCode
                            state
                            street
                        }
                        creditCard {
                            brand
                            expMonth
                            expYear
                            lastFourDigits
                        }
                        customField
                        discordUserId
                        fullName
                        metadata
                        phoneNumber
                        stripeCustomerId
                        totalOrders
                        totalSpendCents
                        trackingParams
                        unrestrictedAccess
                        username
                    }
                }
            }
        }
        """
