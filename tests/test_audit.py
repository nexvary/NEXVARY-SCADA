from nexvary_scada.services.audit import AuditLog


def test_audit_records_action():
    audit = AuditLog()
    audit.record(operator="mohamed", role="operator", action="tag.write", target="pump", success=True, detail={"value": True})
    row = audit.recent()[0]
    assert row["operator"] == "mohamed"
    assert row["success"] is True
    assert row["detail"]["value"] is True
