# Gas Town Configuration

## Project Overview
Treasury Short Duration Scraper - A Lambda function that fetches short-duration Treasury rates from the Treasury.gov FiscalData API.

## Instructions for The Mayor

### Project Context
This is an AWS Lambda function written in Python that:
- Fetches Treasury bill rates from the Treasury.gov FiscalData API
- - Filters for short-duration securities (4-Week, 8-Week, 13-Week, 17-Week, 26-Week, 52-Week Treasury Bills)
  - - Returns deduplicated results as JSON with CORS headers enabled
   
    - ### Code Standards
    - - Python 3.14 runtime
      - - No external dependencies (uses only stdlib: json, urllib.request, datetime)
        - - Lambda handler signature: `lambda_handler(event, context)`
          - - Must return proper HTTP response format with statusCode, headers, and body
           
            - ### API Details
            - - **Endpoint**: Treasury.gov FiscalData API
              - - **Data Source**: Average Interest Rates on U.S. Treasury Securities
                - - **Filter**: Last 30 days of data
                  - - **Rate Limiting**: Respect API limits, use User-Agent header
                   
                    - ### Testing
                    - - Function URL available for direct HTTP invocation
                      - - Test with empty event: `{}`
                        - - Expected response: JSON with `short_duration_rates` array
                         
                          - ### Deployment
                          - - Region: us-east-2 (Ohio)
                            - - Function Name: treasury-short-duration-scraper
                              - - Runtime: Python 3.14
                                - - Architecture: x86_64
                                 
                                  - ### Priorities
                                  - 1. Maintain API reliability and error handling
                                    2. 2. Keep response times under 10 seconds (current timeout)
                                       3. 3. Ensure CORS headers for frontend compatibility
                                          4. 4. Deduplicate results by security type
                                            
                                             5. ### Known Issues
                                             6. - None currently - monitor for API changes from Treasury.gov
                                               
                                                - ### Future Enhancements
                                                - - Add caching layer (DynamoDB or ElastiCache)
                                                  - - Expand to include medium-duration securities
                                                    - - Add historical trend analysis
                                                      - - Implement rate change alerts
