"""
Analytics API endpoints - Advanced analytics and business intelligence

Provides time-series data, cohort analysis, conversion funnels,
engagement patterns, revenue forecasting, and data export.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional, Literal
from datetime import datetime
import io

from app.db.session import get_db
from app.api.deps import get_admin_user
from app.models.user import User
from app.services.analytics_service import AnalyticsService


router = APIRouter()


@router.get("/timeseries")
async def get_timeseries_data(
    metric: str = Query(..., description="Metric to track (signups, readings, revenue, engagement, chat_messages, journal_entries)"),
    period: Literal["daily", "weekly", "monthly"] = Query("daily", description="Time period granularity"),
    days_back: int = Query(30, ge=1, le=365, description="Number of days to look back"),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get time-series data for charts

    **Admin only** 🔐

    **Query Parameters:**
    - **metric**: Metric to track (signups, readings, revenue, engagement, chat_messages, journal_entries)
    - **period**: Time period (daily/weekly/monthly, default: daily)
    - **days_back**: Number of days to look back (default: 30)

    **Returns:**
    Time-series data with dates and values for charting

    **Example Response:**
    ```json
    {
      "metric": "signups",
      "period": "daily",
      "data": [
        {
          "date": "2026-01-01",
          "value": 24
        },
        {
          "date": "2026-01-02",
          "value": 31
        }
      ]
    }
    ```

    **Supported Metrics:**
    - signups: New user registrations
    - readings: Reading requests
    - revenue: Estimated revenue from subscriptions
    - engagement: Active users
    - chat_messages: Chat activity
    - journal_entries: Journal entries

    **Use Cases:**
    - Line charts for tracking trends
    - Bar charts for comparisons
    - Dashboard widgets
    """

    analytics_service = AnalyticsService(db)

    try:
        data = await analytics_service.get_timeseries_data(
            metric=metric,
            period=period,
            days_back=days_back
        )
        return data

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve timeseries data: {str(e)}"
        )


@router.get("/cohorts")
async def get_cohort_analysis(
    weeks_back: int = Query(12, ge=1, le=52, description="Number of weeks to analyze"),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get cohort retention analysis

    **Admin only** 🔐

    Analyzes user retention by signup cohort (grouped by week).
    Shows how many users from each cohort remain active over time.

    **Query Parameters:**
    - **weeks_back**: Number of weeks to analyze (default: 12)

    **Returns:**
    Cohort retention matrix with weekly retention rates

    **Example Response:**
    ```json
    {
      "cohorts": [
        {
          "cohort_week": "2026-01-06",
          "cohort_size": 45,
          "retention": [
            {"week": 0, "active_users": 45, "retention_rate": 100.0},
            {"week": 1, "active_users": 32, "retention_rate": 71.1},
            {"week": 2, "active_users": 28, "retention_rate": 62.2}
          ]
        }
      ]
    }
    ```

    **Use Cases:**
    - Measure user retention over time
    - Compare cohort performance
    - Identify retention drop-off points
    - Calculate lifetime value by cohort
    """

    admin_service = AnalyticsService(db)

    try:
        cohorts = await admin_service.get_cohort_analysis(weeks_back=weeks_back)
        return cohorts

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate cohort analysis: {str(e)}"
        )


@router.get("/funnel")
async def get_conversion_funnel(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get conversion funnel analysis

    **Admin only** 🔐

    **Returns:**
    Conversion funnel data tracking user journey:
    - Signup (100% baseline)
    - First Reading (conversion rate from signup)
    - Premium Upgrade (conversion rate from signup)

    **Example Response:**
    ```json
    {
      "period": "last_30_days",
      "stages": [
        {
          "stage": "signup",
          "users": 1000,
          "conversion_rate": 100.0
        },
        {
          "stage": "first_reading",
          "users": 650,
          "conversion_rate": 65.0
        },
        {
          "stage": "premium",
          "users": 150,
          "conversion_rate": 15.0
        }
      ],
      "overall_conversion": 15.0
    }
    ```

    **Use Cases:**
    - Identify drop-off points in user journey
    - Optimize conversion funnel
    - A/B testing analysis
    """

    analytics_service = AnalyticsService(db)

    try:
        funnel = await analytics_service.get_conversion_funnel()
        return funnel

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve funnel data: {str(e)}"
        )


@router.get("/engagement")
async def get_engagement_patterns(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get user engagement patterns

    **Admin only** 🔐

    **Returns:**
    Engagement metrics including:
    - Hourly activity patterns (0-23)
    - Daily activity patterns (Monday-Sunday)
    - Reading type preferences

    **Example Response:**
    ```json
    {
      "period": "last_30_days",
      "hourly_activity": [
        {"hour": 9, "activity_count": 245},
        {"hour": 10, "activity_count": 312},
        ...
      ],
      "daily_activity": [
        {"day": "Monday", "activity_count": 523},
        ...
      ],
      "reading_preferences": [
        {"type": "COFFEE", "count": 450},
        {"type": "TAROT", "count": 678}
      ]
    }
    ```

    **Usage:** Use this data to understand when users are most active
    and what types of readings they prefer.
    """

    admin_service = AnalyticsService(db)

    try:
        patterns = await admin_service.get_engagement_patterns()
        return patterns

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve engagement patterns: {str(e)}"
        )


@router.get("/revenue/forecast")
async def get_revenue_forecast(
    months: int = Query(3, ge=1, le=12, description="Months to forecast"),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get revenue forecast

    **Admin only** 🔐

    **Query Parameters:**
    - **months**: Number of months to forecast (1-12, default: 3)

    **Returns:**
    Revenue projections based on current growth trends

    **Example Response:**
    ```json
    {
      "current_mrr": 3511.53,
      "growth_rate_3mo": 23.4,
      "monthly_growth_rate": 7.8,
      "forecast": [
        {
          "month": "2026-02",
          "projected_mrr": 3785.23,
          "projected_arr": 45422.76
        },
        {
          "month": "2026-03",
          "projected_mrr": 4080.12,
          "projected_arr": 48961.44
        }
      ]
    }
    ```

    **Methodology:**
    - Calculates current MRR from active subscriptions
    - Measures 3-month historical growth rate
    - Projects forward using linear growth model
    """

    analytics_service = AnalyticsService(db)

    try:
        forecast = await analytics_service.get_revenue_forecast(months_ahead=months)
        return forecast

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate revenue forecast: {str(e)}"
        )


@router.get("/export")
async def export_analytics_data(
    data_type: str = Query(..., description="Data type to export (users, readings, revenue)"),
    format: Literal["json", "csv"] = Query("json", description="Export format"),
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Export analytics data

    **Admin only** 🔐

    **Query Parameters:**
    - **data_type**: Type of data (users, readings, revenue) - **required**
    - **format**: Export format (json or csv, default: json)
    - **start_date**: Start date filter (ISO format, e.g., 2026-01-01)
    - **end_date**: End date filter (ISO format)

    **Returns:**
    Exported data in requested format

    **Supported Data Types:**
    - **users**: User list with signup data
    - **readings**: Reading history
    - **revenue**: Revenue data (future)

    **Example:**
    `/api/v1/analytics/export?data_type=users&format=csv&start_date=2026-01-01`
    """

    analytics_service = AnalyticsService(db)

    try:
        # Parse dates
        start_dt = datetime.fromisoformat(start_date) if start_date else None
        end_dt = datetime.fromisoformat(end_date) if end_date else None

        export = await analytics_service.export_data(
            data_type=data_type,
            format=format,
            start_date=start_dt,
            end_date=end_dt
        )

        return export

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export data: {str(e)}"
        )
