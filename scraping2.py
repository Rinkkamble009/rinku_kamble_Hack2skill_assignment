import requests
import csv


CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'

ACCESS_TOKEN = 'your_access_token'  

def get_company_data(company_ids):
    """
    Fetches company data for multiple companies using LinkedIn API.
    :param company_ids: List of LinkedIn company IDs.
    :return: List of dictionaries containing company data.
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    base_url = "https://api.linkedin.com/v2/organizations/"
    company_data_list = []

    for company_id in company_ids:
        url = f"{base_url}{company_id}"
        print(f"Fetching data for company ID: {company_id}")
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            company_data = {
                "Company Name": data.get("localizedName", "N/A"),
                "Address": data.get("headquarter", {}).get("address", "N/A") if data.get("headquarter") else "N/A",
                "Website": data.get("website", "N/A"),
                "Phone Numbers": ", ".join(data.get("phoneNumbers", [])) if data.get("phoneNumbers") else "N/A",
                "Industry": ", ".join(data.get("industries", [])) if data.get("industries") else "N/A",
            }
            company_data_list.append(company_data)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            continue

    return company_data_list

def save_to_csv(data, filename):
    """
    Saves data to a CSV file.
    :param data: List of dictionaries containing company data.
    :param filename: Name of the CSV file.
    """
    if not data:
        print("No data to save.")
        return
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {filename}.")

if __name__ == "__main__":
    company_ids = ["microsoft", "google", "skype"]  

    company_data = get_company_data(company_ids)

   
    save_to_csv(company_data, "linkedin_company_data.csv")
