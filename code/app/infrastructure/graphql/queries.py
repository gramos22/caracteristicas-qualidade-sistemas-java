SEARCH_REPOS_PAGINATED = """
query($q: String!, $first: Int!, $after: String) {
  search(query: $q, type: REPOSITORY, first: $first, after: $after) {
    repositoryCount
    pageInfo { 
      endCursor 
      hasNextPage 
    }
    nodes {
      ... on Repository {
        name
        url
        stargazerCount
        createdAt
        releases { 
          totalCount 
        }
      }
    }
  }
}
"""