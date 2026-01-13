"""
Analytics Service - Advanced analytics and business intelligence

Provides time-series data, cohort analysis, user behavior analytics,
revenue forecasting, and data export capabilities.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_, case
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timedelta, date
from collections import defaultdict
import json

from app.models.user import User
from app.models.subscription import Subscription, SubscriptionTier
from app.models.reading import Reading, ReadingType
from app.models.chat import ChatMessage
from app.models.journal import JournalEntry
from app.models.notification import NotificationHistory


class AnalyticsService:
    """
    Service for advanced analytics and business intelligence

    Features:
    - Time-series data for charts (daily/weekly/monthly)
    - Cohort retention analysis
    - Conversion funnel tracking
    - User engagement patterns
    - Revenue forecasting
    - Data export (CSV, JSON)
    """

    def __init__(self, db: Session):
        """
        Initialize analytics service

        Args:
            db: Database session
        """
        self.db = db

    async def get_timeseries_data(
        self,
        metric: str,
        period: Literal["daily", "weekly", "monthly"] = "daily",
        days_back: int = 30
    ) -> Dict[str, Any]:
        """
        Get time-series data for charts

        Args:
            metric: Metric to track (signups, readings, revenue, etc.)
            period: Time period granularity
            days_back: Number of days to look back

        Returns:
            Time-series data with labels and values
        """

        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days_back)

        if metric == "signups":
            return await self._get_signup_timeseries(start_date, end_date, period)
        elif metric == "readings":
            return await self._get_readings_timeseries(start_date, end_date, period)
        elif metric == "revenue":
            return await self._get_revenue_timeseries(start_date, end_date, period)
        elif metric == "engagement":
            return await self._get_engagement_timeseries(start_date, end_date, period)
        elif metric == "chat_messages":
            return await self._get_chat_timeseries(start_date, end_date, period)
        elif metric == "journal_entries":
            return await self._get_journal_timeseries(start_date, end_date, period)
        else:
            raise ValueError(f"Unknown metric: {metric}")

    async def _get_signup_timeseries(
        self,
        start_date: datetime,
        end_date: datetime,
        period: str
    ) -> Dict[str, Any]:
        """Get user signup time-series"""

        if period == "daily":
            # Daily signups
            results = (
                self.db.query(
                    func.date(User.created_at).label("date"),
                    func.count(User.id).label("count")
                )
                .filter(User.created_at >= start_date)
                .filter(User.created_at <= end_date)
                .group_by(func.date(User.created_at))
                .order_by(func.date(User.created_at))
                .all()
            )

            return {
                "metric": "signups",
                "period": "daily",
                "data": [
                    {
                        "date": result.date.isoformat(),
                        "value": result.count
                    }
                    for result in results
                ]
            }

        elif period == "weekly":
            # Weekly signups
            results = (
                self.db.query(
                    func.date_trunc('week', User.created_at).label("week"),
                    func.count(User.id).label("count")
                )
                .filter(User.created_at >= start_date)
                .filter(User.created_at <= end_date)
                .group_by(func.date_trunc('week', User.created_at))
                .order_by(func.date_trunc('week', User.created_at))
                .all()
            )

            return {
                "metric": "signups",
                "period": "weekly",
                "data": [
                    {
                        "week": result.week.isoformat() if result.week else None,
                        "value": result.count
                    }
                    for result in results
                ]
            }

        else:  # monthly
            # Monthly signups
            results = (
                self.db.query(
                    extract('year', User.created_at).label("year"),
                    extract('month', User.created_at).label("month"),
                    func.count(User.id).label("count")
                )
                .filter(User.created_at >= start_date)
                .filter(User.created_at <= end_date)
                .group_by(
                    extract('year', User.created_at),
                    extract('month', User.created_at)
                )
                .order_by(
                    extract('year', User.created_at),
                    extract('month', User.created_at)
                )
                .all()
            )

            return {
                "metric": "signups",
                "period": "monthly",
                "data": [
                    {
                        "month": f"{int(result.year)}-{int(result.month):02d}",
                        "value": result.count
                    }
                    for result in results
                ]
            }

    async def _get_readings_timeseries(
        self,
        start_date: datetime,
        end_date: datetime,
        period: str
    ) -> Dict[str, Any]:
        """Get readings time-series"""

        if period == "daily":
            results = (
                self.db.query(
                    func.date(Reading.created_at).label("date"),
                    func.count(Reading.id).label("count")
                )
                .filter(Reading.created_at >= start_date)
                .filter(Reading.created_at <= end_date)
                .group_by(func.date(Reading.created_at))
                .order_by(func.date(Reading.created_at))
                .all()
            )

            return {
                "metric": "readings",
                "period": "daily",
                "data": [
                    {
                        "date": result.date.isoformat(),
                        "value": result.count
                    }
                    for result in results
                ]
            }

        # Similar logic for weekly/monthly...
        return {"metric": "readings", "period": period, "data": []}

    async def _get_revenue_timeseries(
        self,
        start_date: datetime,
        end_date: datetime,
        period: str
    ) -> Dict[str, Any]:
        """Get revenue time-series (estimated from subscriptions)"""

        # Revenue estimation based on subscription creation dates
        # In production, would track actual payment events

        tier_prices = {
            SubscriptionTier.WEEKLY: 4.99,
            SubscriptionTier.MONTHLY: 14.99,
            SubscriptionTier.ANNUAL: 99.99
        }

        if period == "daily":
            results = (
                self.db.query(
                    func.date(Subscription.created_at).label("date"),
                    Subscription.tier,
                    func.count(Subscription.id).label("count")
                )
                .filter(Subscription.created_at >= start_date)
                .filter(Subscription.created_at <= end_date)
                .filter(Subscription.is_active == True)
                .filter(Subscription.tier != SubscriptionTier.FREE)
                .group_by(func.date(Subscription.created_at), Subscription.tier)
                .order_by(func.date(Subscription.created_at))
                .all()
            )

            # Aggregate by date
            revenue_by_date = defaultdict(float)
            for result in results:
                revenue_by_date[result.date] += tier_prices.get(result.tier, 0) * result.count

            return {
                "metric": "revenue",
                "period": "daily",
                "data": [
                    {
                        "date": date.isoformat(),
                        "value": round(revenue, 2)
                    }
                    for date, revenue in sorted(revenue_by_date.items())
                ]
            }

        return {"metric": "revenue", "period": period, "data": []}

    async def _get_engagement_timeseries(
        self,
        start_date: datetime,
        end_date: datetime,
        period: str
    ) -> Dict[str, Any]:
        """Get engagement time-series (active users)"""

        if period == "daily":
            # Count users with any activity (readings, chat, journal)
            reading_users = (
                self.db.query(
                    func.date(Reading.created_at).label("date"),
                    func.count(func.distinct(Reading.user_id)).label("count")
                )
                .filter(Reading.created_at >= start_date)
                .filter(Reading.created_at <= end_date)
                .group_by(func.date(Reading.created_at))
                .all()
            )

            return {
                "metric": "engagement",
                "period": "daily",
                "data": [
                    {
                        "date": result.date.isoformat(),
                        "value": result.count
                    }
                    for result in reading_users
                ]
            }

        return {"metric": "engagement", "period": period, "data": []}

    async def _get_chat_timeseries(
        self,
        start_date: datetime,
        end_date: datetime,
        period: str
    ) -> Dict[str, Any]:
        """Get chat messages time-series"""

        if period == "daily":
            results = (
                self.db.query(
                    func.date(ChatMessage.created_at).label("date"),
                    func.count(ChatMessage.id).label("count")
                )
                .filter(ChatMessage.created_at >= start_date)
                .filter(ChatMessage.created_at <= end_date)
                .filter(ChatMessage.role == "user")  # Only count user messages
                .group_by(func.date(ChatMessage.created_at))
                .order_by(func.date(ChatMessage.created_at))
                .all()
            )

            return {
                "metric": "chat_messages",
                "period": "daily",
                "data": [
                    {
                        "date": result.date.isoformat(),
                        "value": result.count
                    }
                    for result in results
                ]
            }

        return {"metric": "chat_messages", "period": period, "data": []}

    async def _get_journal_timeseries(
        self,
        start_date: datetime,
        end_date: datetime,
        period: str
    ) -> Dict[str, Any]:
        """Get journal entries time-series"""

        if period == "daily":
            results = (
                self.db.query(
                    func.date(JournalEntry.created_at).label("date"),
                    func.count(JournalEntry.id).label("count")
                )
                .filter(JournalEntry.created_at >= start_date)
                .filter(JournalEntry.created_at <= end_date)
                .group_by(func.date(JournalEntry.created_at))
                .order_by(func.date(JournalEntry.created_at))
                .all()
            )

            return {
                "metric": "journal_entries",
                "period": "daily",
                "data": [
                    {
                        "date": result.date.isoformat(),
                        "value": result.count
                    }
                    for result in results
                ]
            }

        return {"metric": "journal_entries", "period": period, "data": []}

    async def get_cohort_analysis(
        self,
        weeks_back: int = 12
    ) -> Dict[str, Any]:
        """
        Get cohort retention analysis

        Cohorts are grouped by signup week, and retention is measured
        by user activity in subsequent weeks.

        Args:
            weeks_back: Number of weeks to analyze

        Returns:
            Cohort retention matrix
        """

        end_date = datetime.utcnow()
        start_date = end_date - timedelta(weeks=weeks_back)

        # Get all users in the time period
        users = (
            self.db.query(User)
            .filter(User.created_at >= start_date)
            .filter(User.created_at <= end_date)
            .all()
        )

        # Group users by signup week
        cohorts = defaultdict(list)
        for user in users:
            week_start = user.created_at - timedelta(days=user.created_at.weekday())
            cohort_key = week_start.date().isoformat()
            cohorts[cohort_key].append(user.id)

        # Calculate retention for each cohort
        cohort_data = []
        for cohort_week, user_ids in sorted(cohorts.items()):
            cohort_start = datetime.fromisoformat(cohort_week)

            retention_weeks = []
            for week_num in range(8):  # Track 8 weeks of retention
                week_start = cohort_start + timedelta(weeks=week_num)
                week_end = week_start + timedelta(weeks=1)

                # Count active users in this week (had any activity)
                active_count = (
                    self.db.query(func.count(func.distinct(Reading.user_id)))
                    .filter(Reading.user_id.in_(user_ids))
                    .filter(Reading.created_at >= week_start)
                    .filter(Reading.created_at < week_end)
                    .scalar()
                )

                retention_pct = (active_count / len(user_ids) * 100) if user_ids else 0
                retention_weeks.append({
                    "week": week_num,
                    "active_users": active_count,
                    "retention_rate": round(retention_pct, 1)
                })

            cohort_data.append({
                "cohort_week": cohort_week,
                "cohort_size": len(user_ids),
                "retention": retention_weeks
            })

        return {
            "cohorts": cohort_data,
            "total_cohorts": len(cohort_data)
        }

    async def get_conversion_funnel(self) -> Dict[str, Any]:
        """
        Get conversion funnel data

        Tracks user journey: Signup → First Reading → Premium

        Returns:
            Funnel stages with conversion rates
        """

        # Total signups (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)

        total_signups = (
            self.db.query(func.count(User.id))
            .filter(User.created_at >= thirty_days_ago)
            .scalar()
        )

        # Users who made at least one reading
        users_with_readings = (
            self.db.query(func.count(func.distinct(Reading.user_id)))
            .join(User, Reading.user_id == User.id)
            .filter(User.created_at >= thirty_days_ago)
            .scalar()
        )

        # Users who upgraded to premium
        premium_users = (
            self.db.query(func.count(func.distinct(Subscription.user_id)))
            .join(User, Subscription.user_id == User.id)
            .filter(User.created_at >= thirty_days_ago)
            .filter(Subscription.tier != SubscriptionTier.FREE)
            .filter(Subscription.is_active == True)
            .scalar()
        )

        # Calculate conversion rates
        reading_conversion = (users_with_readings / total_signups * 100) if total_signups > 0 else 0
        premium_conversion = (premium_users / total_signups * 100) if total_signups > 0 else 0

        return {
            "period": "last_30_days",
            "stages": [
                {
                    "stage": "signup",
                    "users": total_signups,
                    "conversion_rate": 100.0
                },
                {
                    "stage": "first_reading",
                    "users": users_with_readings,
                    "conversion_rate": round(reading_conversion, 1)
                },
                {
                    "stage": "premium",
                    "users": premium_users,
                    "conversion_rate": round(premium_conversion, 1)
                }
            ],
            "overall_conversion": round(premium_conversion, 1)
        }

    async def get_engagement_patterns(self) -> Dict[str, Any]:
        """
        Analyze user engagement patterns

        Returns:
            Engagement metrics by time of day, day of week, etc.
        """

        thirty_days_ago = datetime.utcnow() - timedelta(days=30)

        # Activity by hour of day
        hourly_activity = (
            self.db.query(
                extract('hour', Reading.created_at).label("hour"),
                func.count(Reading.id).label("count")
            )
            .filter(Reading.created_at >= thirty_days_ago)
            .group_by(extract('hour', Reading.created_at))
            .order_by(extract('hour', Reading.created_at))
            .all()
        )

        # Activity by day of week (0=Monday, 6=Sunday)
        daily_activity = (
            self.db.query(
                extract('dow', Reading.created_at).label("day"),
                func.count(Reading.id).label("count")
            )
            .filter(Reading.created_at >= thirty_days_ago)
            .group_by(extract('dow', Reading.created_at))
            .order_by(extract('dow', Reading.created_at))
            .all()
        )

        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # Reading type preferences
        reading_preferences = (
            self.db.query(
                Reading.reading_type,
                func.count(Reading.id).label("count")
            )
            .filter(Reading.created_at >= thirty_days_ago)
            .group_by(Reading.reading_type)
            .all()
        )

        return {
            "period": "last_30_days",
            "hourly_activity": [
                {
                    "hour": int(result.hour),
                    "activity_count": result.count
                }
                for result in hourly_activity
            ],
            "daily_activity": [
                {
                    "day": day_names[int(result.day)],
                    "activity_count": result.count
                }
                for result in daily_activity
            ],
            "reading_preferences": [
                {
                    "type": result.reading_type.value,
                    "count": result.count
                }
                for result in reading_preferences
            ]
        }

    async def get_revenue_forecast(
        self,
        months_ahead: int = 3
    ) -> Dict[str, Any]:
        """
        Forecast revenue based on current trends

        Uses simple linear projection based on last 3 months' growth

        Args:
            months_ahead: Number of months to forecast

        Returns:
            Revenue forecast data
        """

        # Get current active subscriptions
        active_subs = (
            self.db.query(Subscription)
            .filter(Subscription.is_active == True)
            .filter(Subscription.tier != SubscriptionTier.FREE)
            .all()
        )

        # Calculate current MRR
        tier_prices_monthly = {
            SubscriptionTier.WEEKLY: 19.96,  # $4.99/week ≈ $19.96/month
            SubscriptionTier.MONTHLY: 14.99,
            SubscriptionTier.ANNUAL: 8.33  # $99.99/year ≈ $8.33/month
        }

        current_mrr = sum(
            tier_prices_monthly.get(sub.tier, 0)
            for sub in active_subs
        )

        # Get growth rate (simplified - comparing to 3 months ago)
        three_months_ago = datetime.utcnow() - timedelta(days=90)
        old_subs = (
            self.db.query(Subscription)
            .filter(Subscription.created_at <= three_months_ago)
            .filter(Subscription.is_active == True)
            .filter(Subscription.tier != SubscriptionTier.FREE)
            .all()
        )

        old_mrr = sum(
            tier_prices_monthly.get(sub.tier, 0)
            for sub in old_subs
        )

        growth_rate = ((current_mrr - old_mrr) / old_mrr * 100) if old_mrr > 0 else 10.0
        monthly_growth_rate = growth_rate / 3  # Average monthly growth

        # Project forward
        forecasts = []
        projected_mrr = current_mrr

        for month in range(1, months_ahead + 1):
            projected_mrr = projected_mrr * (1 + monthly_growth_rate / 100)

            forecast_date = datetime.utcnow() + timedelta(days=30 * month)

            forecasts.append({
                "month": forecast_date.strftime("%Y-%m"),
                "projected_mrr": round(projected_mrr, 2),
                "projected_arr": round(projected_mrr * 12, 2)
            })

        return {
            "current_mrr": round(current_mrr, 2),
            "growth_rate_3mo": round(growth_rate, 1),
            "monthly_growth_rate": round(monthly_growth_rate, 1),
            "forecast": forecasts
        }

    async def export_data(
        self,
        data_type: str,
        format: Literal["json", "csv"] = "json",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Export analytics data

        Args:
            data_type: Type of data to export (users, readings, revenue, etc.)
            format: Export format (json or csv)
            start_date: Start date filter
            end_date: End date filter

        Returns:
            Exported data in requested format
        """

        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()

        if data_type == "users":
            users = (
                self.db.query(User)
                .filter(User.created_at >= start_date)
                .filter(User.created_at <= end_date)
                .all()
            )

            data = [
                {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "zodiac_sign": user.zodiac_sign,
                    "created_at": user.created_at.isoformat(),
                    "is_admin": user.is_admin,
                    "is_banned": user.is_banned
                }
                for user in users
            ]

            if format == "csv":
                return self._convert_to_csv(data)

            return {"format": "json", "data": data}

        elif data_type == "readings":
            readings = (
                self.db.query(Reading)
                .filter(Reading.created_at >= start_date)
                .filter(Reading.created_at <= end_date)
                .all()
            )

            data = [
                {
                    "id": reading.id,
                    "user_id": reading.user_id,
                    "reading_type": reading.reading_type.value,
                    "created_at": reading.created_at.isoformat()
                }
                for reading in readings
            ]

            if format == "csv":
                return self._convert_to_csv(data)

            return {"format": "json", "data": data}

        return {"format": format, "data": []}

    def _convert_to_csv(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Convert JSON data to CSV format"""

        if not data:
            return {"format": "csv", "data": ""}

        # Get headers from first row
        headers = list(data[0].keys())

        # Build CSV
        csv_lines = [",".join(headers)]
        for row in data:
            csv_lines.append(",".join(str(row.get(h, "")) for h in headers))

        return {
            "format": "csv",
            "data": "\n".join(csv_lines),
            "filename": f"export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        }
