import json
import urllib.request
from datetime import datetime, timedelta


def lambda_handler(event, context):
      """Fetches short-duration Treasury rates from Treasury.gov API."""

    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    url = f"https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?filter=record_date:gte:{start_date},record_date:lte:{end_date}&sort=-record_date&page[size]=100"

    try:
              req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
              with urllib.request.urlopen(req, timeout=10) as response:
                            data = json.loads(response.read().decode())

              # Filter for short-duration securities
              short_duration = ['Treasury Bills', '4-Week', '8-Week', '13-Week', '17-Week', '26-Week', '52-Week']

        results = []
        seen = set()

        for record in data.get('data', []):
                      security = record.get('security_desc', '')
                      if any(term in security for term in short_duration):
                                        key = security
                                        if key not in seen:
                                                              seen.add(key)
                                                              results.append({
                                                                  'security': security,
                                                                  'rate': record.get('avg_interest_rate_amt'),
                                                                  'date': record.get('record_date')
                                                              })

                                return {
                                              'statusCode': 200,
                                              'headers': {
                                                                'Content-Type': 'application/json',
                                                                'Access-Control-Allow-Origin': '*'
                                              },
                                              'body': json.dumps({
                                                                'source': 'Treasury.gov FiscalData API',
                                                                'fetched_at': datetime.now().isoformat(),
                                                                'short_duration_rates': results
                                              })
                                }

except Exception as e:
        return {
                      'statusCode': 500,
                      'headers': {
                                        'Content-Type': 'application/json',
                                        'Access-Control-Allow-Origin': '*'
                      },
                      'body': json.dumps({'error': str(e)})
        }
