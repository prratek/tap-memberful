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
        th.Property(
            "trackingParams",
            th.ObjectType(
                th.Property("referrer", th.StringType),
                th.Property("utm_source", th.StringType),
                th.Property("utm_medium", th.StringType),
                th.Property("utm_campaign", th.StringType),
            )
        ),
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


class OrdersStream(MemberfulStream):
    """Define custom stream."""
    name = "orders"
    primary_keys = ["id"]

    schema = th.PropertiesList(
        th.Property("uuid", th.StringType),
        th.Property("createdAt", th.IntegerType),
        th.Property(
            "coupon",
            th.ObjectType(
                th.Property("id", th.StringType),
            )
        ),
        th.Property("couponDiscountAmountCents", th.IntegerType),
        th.Property("currency", th.StringType),
        th.Property(
            "member",
            th.ObjectType(
                th.Property("id", th.StringType),
            )
        ),
        th.Property(
            "purchasable",
            th.ObjectType(
                th.Property("id", th.StringType),
            )
        ),
        th.Property("purchasableType", th.StringType),
        th.Property("status", th.StringType),
        th.Property(
            "subscription",
            th.ObjectType(
                th.Property("id", th.StringType),
            )
        ),
        th.Property("taxAmountCents", th.IntegerType),
        th.Property("totalCents", th.IntegerType),
        th.Property("type", th.StringType),
    ).to_dict()

    query = """
        query ($afterCursor: String!) {
            orders(after: $afterCursor) {
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                }
                edges {
                    node {
                        uuid
                        createdAt
                        coupon {
                            id
                        }
                        couponDiscountAmountCents
                        currency
                        member {
                            id
                        }
                        purchasable {
                            ... on Download {
                                id
                            }
                            ... on Plan {
                                id
                            }
                        }
                        purchasableType
                        status
                        subscription {
                            id
                        }
                        taxAmountCents
                        totalCents
                        type
                    }
                }
            }
        }
        """


class PlansStream(MemberfulStream):
    """Define custom stream."""
    name = "plans"
    primary_keys = ["id"]

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("additionalMemberPriceCents", th.IntegerType),
        th.Property("afterCheckoutRedirectUrl", th.StringType),
        th.Property("forSale", th.BooleanType),
        th.Property("freeTrialType", th.StringType),
        th.Property("includedMembers", th.IntegerType),
        th.Property("intervalCount", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property(
            "planGroup",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
            )
        ),
        th.Property("priceCents", th.IntegerType),
        th.Property("renewalDay", th.IntegerType),
        th.Property("renewalMonth", th.IntegerType),
        th.Property("requireAddress", th.BooleanType),
        th.Property("slug", th.StringType),
        th.Property("startingMonthForQuarterlyDateBasedPlans", th.IntegerType),
        th.Property("taxable", th.BooleanType),
        th.Property("type", th.StringType),
    ).to_dict()

    query = """
        query {
            plans {
                id
                additionalMemberPriceCents
                afterCheckoutRedirectUrl
                forSale
                freeTrialType
                includedMembers
                intervalCount
                intervalUnit
                name
                planGroup {
                    id
                    name
                }
                priceCents
                renewalDay
                renewalMonth
                requireAddress
                slug
                startingMonthForQuarterlyDateBasedPlans
                taxable
                type
            }
        }
        """


class SubscriptionsStream(MemberfulStream):
    """Define custom stream."""
    name = "subscriptions"
    primary_keys = ["id"]

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("createdAt", th.IntegerType),
        th.Property("activatedAt", th.IntegerType),
        th.Property("expiresAt", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property("additionalMembers", th.IntegerType),
        th.Property("autorenew", th.BooleanType),
        th.Property(
            "coupon",
            th.ObjectType(
                th.Property("id", th.StringType),
            )
        ),
        th.Property(
            "member",
            th.ObjectType(
                th.Property("id", th.StringType),
            )
        ),
        th.Property("pastDue", th.BooleanType),
        th.Property(
            "plan",
            th.ObjectType(
                th.Property("id", th.StringType),
            )
        ),
        th.Property("trialEndAt", th.IntegerType),
        th.Property("trialStartAt", th.IntegerType),
    ).to_dict()

    query = """
        query ($afterCursor: String!) {
            subscriptions(after: $afterCursor) {
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                }
                edges {
                    node {
                        id
                        createdAt
                        activatedAt
                        expiresAt
                        active
                        additionalMembers
                        autorenew
                        coupon {
                            id
                        }
                        member {
                            id
                        }
                        pastDue
                        plan {
                            id
                        }
                        trialEndAt
                        trialStartAt
                    }
                }
            }
        }
        """
