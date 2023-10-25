from github_project_assistant import create_issue, update_issue,test
assets = {
    "owner": "wzfukui",
    "repository": "OctoMation",
    "pat_token": "ghp_8nRqCb***"
}
params ={
    "issue_number": 19,
    "issue_title": "Test Title updated",
    "issue_body": "Test Body  updated",
    "issue_label": "bug",
    "issue_state": "open",
    "issue_state_reason": "completed"
}
context_info = None

# ret = create_issue(params, assets, context_info)
# print(ret)

# ret = test(params, assets, context_info)
# print(ret)

# ret = update_issue(params, assets, context_info)
# print(ret)
