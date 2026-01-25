# Treasury Short Duration Scraper

AWS Lambda function that fetches short-duration Treasury rates from the Treasury.gov FiscalData API.

## Features

- Fetches Treasury bill rates (4-Week through 52-Week)
- - Returns deduplicated, sorted results
  - - CORS-enabled for frontend integration
    - - Zero external dependencies
     
      - ## API Response
     
      - ```json
        {
          "source": "Treasury.gov FiscalData API",
          "fetched_at": "2026-01-25T12:00:00",
          "short_duration_rates": [
            {
              "security": "Treasury Bills",
              "rate": "5.250",
              "date": "2026-01-24"
            }
          ]
        }
        ```

        ## Deployment

        Deployed as AWS Lambda with Function URL enabled.

        **Region**: us-east-2
        **Runtime**: Python 3.14

        ## Gas Town Integration

        This project is configured for [Gas Town](https://gas-town-ui-poc.onrender.com/) multi-agent orchestration. See `GASTOWN.md` for agent configuration.
