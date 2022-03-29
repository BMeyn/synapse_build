# Release Notes 
## Pull Requests
{{#forEach runDetails.pull_requests}}
**{{this.number}}** {{this.title}}
### Commits
  {{#forEach this.commits}}
  - **{{this.sha}}** {{this.commit.message}}
  {{/forEach}}
{{/forEach}}