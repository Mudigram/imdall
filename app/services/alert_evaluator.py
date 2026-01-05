def evaluate_alerts(db: Session, website: Website, metrics: WebsiteMetrics):
    alerts = []

    # Downtime alert
    if metrics.consecutive_failures >= 5:
        alerts.append({
            "type": "downtime",
            "severity": "critical",
            "message": f"{website.name} is down"
        })

    # Performance alert
    if metrics.avg_response_time_ms and metrics.avg_response_time_ms > 2000:
        alerts.append({
            "type": "performance",
            "severity": "warning",
            "message": f"{website.name} response time degraded"
        })

    return alerts

def create_alert_if_needed(db, website_id, alert):
    existing = (
        db.query(Alert)
        .filter(
            Alert.website_id == website_id,
            Alert.alert_type == alert["type"],
            Alert.resolved_at.is_(None)
        )
        .first()
    )

    if not existing:
        db.add(Alert(
            website_id=website_id,
            alert_type=alert["type"],
            severity=alert["severity"],
            message=alert["message"]
        ))
        db.commit()
