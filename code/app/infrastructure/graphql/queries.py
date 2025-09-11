SEARCH_REPOS_PAGINATED = """
query($q: String!, $first: Int!, $after: String) {
  search(query: $q, type: REPOSITORY, first: $first, after: $after) {
    repositoryCount
    pageInfo { endCursor hasNextPage }
    edges {
      node {
        ... on Repository {
          name
          stargazerCount
          url
          createdAt
          updatedAt
          releases { totalCount }
          primaryLanguage { name }
          mergedPullRequests: pullRequests(states: MERGED) { totalCount }
          closedIssues: issues(filterBy: { states: CLOSED }) { totalCount }
          totalIssues: issues { totalCount }
        }
      }
    }
  }
}
"""
