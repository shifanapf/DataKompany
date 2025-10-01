import csv
import requests # type: ignore

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Origin': 'https://planningregister.planningsystemni.gov.uk',
    'Referer': 'https://planningregister.planningsystemni.gov.uk/',
    'Request-Id': '|7cf325d37b7e4fff81cbe1fd4b9610d5.1e0e74c2d6eb438a',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'TQ-Tenant': 'cfb86436-414d-4459-9545-93eec37615a2',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'traceparent': '00-7cf325d37b7e4fff81cbe1fd4b9610d5-1e0e74c2d6eb438a-01',
}

params = {
    'SearchStatus': 'valid',
    'AuthorityId': '1',
    'DisplayType': 'monthly',
    'PageSize': '10',
    'PageNumber': '1',
    'authorities': '1',
    'dateFrom': '2025-09-09T18:30:00.000Z',
    'dateTo': '2025-09-30T18:30:00.000Z',
    'sortByDescending': 'true',
}


base_url= 'https://api-planningregister-planningportal.pr.tqinfra.co.uk/api/v1/applications/list'
page =1
total_records=0
extracted_data=[]


while True:
    params['PageNumber'] = str(page)
    try: 
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            applications = data.get('groups').get('items')[0].get('applications')
            
            if not applications:
                print(f"No applications found at page {page}")
                break

            
            extracted_data.extend(applications)
            total_records += len(applications)
            
            print(f'Page {page}: Fetched {len(applications)} records: Total records fetched: {total_records}')
            
            if len(applications) < int(params['PageSize']):
                print("Reached last page")
                break
            
            page += 1
            
        else:
            print(f"Error: Status code {response.status_code}")
            break
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        break

if extracted_data:    
    with open('applications.csv', 'w', newline='', encoding='utf-8') as output_file:
        keys = extracted_data[0].keys()
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(extracted_data)
    
    print(f"Successfully saved {total_records} records to applications.csv")
else:
    print("No data to write")

