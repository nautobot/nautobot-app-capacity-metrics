# External Interactions

This document describes external dependencies and prerequisites for this App to operate, including system requirements, API endpoints, interconnection or integrations to other applications or services, and similar topics.

## External System Integrations

### Default Metrics for the application metrics endpoint

The following metrics will be provided via the `/api/plugins/capacity-metrics/app-metrics` endpoint:

```no-highlight
# HELP nautobot_gitrepository_task_stats Per Git repository task statistics
# TYPE nautobot_gitrepository_task_stats gauge
nautobot_gitrepository_task_stats{module="repo1",name="main",status="success"} 1.0
nautobot_gitrepository_task_stats{module="repo1",name="main",status="warning"} 0.0
nautobot_gitrepository_task_stats{module="repo1",name="main",status="failure"} 0.0
nautobot_gitrepository_task_stats{module="repo1",name="main",status="info"} 6.0
nautobot_gitrepository_task_stats{module="repo1",name="total",status="success"} 1.0
nautobot_gitrepository_task_stats{module="repo1",name="total",status="warning"} 0.0
nautobot_gitrepository_task_stats{module="repo1",name="total",status="failure"} 0.0
nautobot_gitrepository_task_stats{module="repo1",name="total",status="info"} 6.0
# HELP nautobot_gitrepository_execution_status Git repository completion status
# TYPE nautobot_gitrepository_execution_status gauge
nautobot_gitrepository_execution_status{module="repo1",status="pending"} 0.0
nautobot_gitrepository_execution_status{module="repo1",status="running"} 0.0
nautobot_gitrepository_execution_status{module="repo1",status="completed"} 1.0
nautobot_gitrepository_execution_status{module="repo1",status="errored"} 0.0
nautobot_gitrepository_execution_status{module="repo1",status="failed"} 0.0
# HELP nautobot_job_task_stats Per Job task statistics
# TYPE nautobot_job_task_stats gauge
nautobot_job_task_stats{module="local/users/CheckUser",name="total",status="success"} 1.0
nautobot_job_task_stats{module="local/users/CheckUser",name="total",status="warning"} 0.0
nautobot_job_task_stats{module="local/users/CheckUser",name="total",status="failure"} 0.0
nautobot_job_task_stats{module="local/users/CheckUser",name="total",status="info"} 0.0
nautobot_job_task_stats{module="local/users/CheckUser",name="test_is_uppercase",status="success"} 1.0
nautobot_job_task_stats{module="local/users/CheckUser",name="test_is_uppercase",status="warning"} 0.0
nautobot_job_task_stats{module="local/users/CheckUser",name="test_is_uppercase",status="failure"} 0.0
nautobot_job_task_stats{module="local/users/CheckUser",name="test_is_uppercase",status="info"} 0.0
# HELP nautobot_job_execution_status Job completion status
# TYPE nautobot_job_execution_status gauge
nautobot_job_execution_status{module="local/users/CheckUser",status="pending"} 0.0
nautobot_job_execution_status{module="local/users/CheckUser",status="running"} 0.0
nautobot_job_execution_status{module="local/users/CheckUser",status="completed"} 1.0
nautobot_job_execution_status{module="local/users/CheckUser",status="errored"} 0.0
nautobot_job_execution_status{module="local/users/CheckUser",status="failed"} 0.0
# HELP nautobot_model_count Per Nautobot Model count
# TYPE nautobot_model_count gauge
nautobot_model_count{app="dcim",name="Site"} 24.0
nautobot_model_count{app="dcim",name="Rack"} 24.0
nautobot_model_count{app="dcim",name="Device"} 46.0
nautobot_model_count{app="ipam",name="IPAddress"} 58.0
nautobot_model_count{app="ipam",name="Prefix"} 18.0
nautobot_model_count{app="extras",name="GitRepository"} 1.0
# HELP nautobot_app_metrics_processing_ms Time in ms to generate the app metrics endpoint
# TYPE nautobot_app_metrics_processing_ms gauge
nautobot_app_metrics_processing_ms 59.48257
```
