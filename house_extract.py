import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_links(pages, base_url):
    extracted_links = []
    count = 0
    for page in pages:
        try:
            response = requests.get(page)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                links = soup.find_all('a')
                for link in links:
                    href = link.get('href')
                    if href and href.startswith('/elan/satilir'):
                        full_link = base_url + href
                        if full_link not in extracted_links:  # Avoid duplicate links
                            count += 1
                            extracted_links.append(full_link)
                print(f'in this {page}, we have {count} links')
            elif response.status_code == 429:
                print(f'Too many requests for page {page}. Waiting...')
                time.sleep(60)  # wait for 1 minute before retrying
                response = requests.get(page)  # retry the request
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    links = soup.find_all('a')
                    for link in links:
                        href = link.get('href')
                        if href and href.startswith('/elan/satilir'):
                            full_link = base_url + href
                            if full_link not in extracted_links:  # Avoid duplicate links
                                count += 1
                                extracted_links.append(full_link)
                    print(f'in this {page}, we have {count} links')
            else:
                print(f'Failed to fetch the web page: {page}, Status code: {response.status_code}')
            count = 0
        except Exception as e:
            print(f"An error occurred while processing page {page}: {e}")
    return extracted_links

def get_all_pages():
    pages = []
    page = 'https://yeniemlak.az/elan/axtar?elan_nov=1&emlak=1&menzil_nov=&qiymet=&qiymet2=&mertebe=&mertebe2=&otaq=&otaq2=&sahe_m=&sahe_m2=&sahe_s=&sahe_s2=&seher%5B%5D=57&page='
    
    for i in range(1, 143):
        pages.append(page + str(i))
    
    return pages

def get_information(links):
    try:
        # Define the expected columns
        columns = ['Qiymet', 'Tarix', 'Baxış', 'Elan', 'Emlak', "Kateqoriya", 'Mərtəbə', "Sahə", 'Otaq sayı', 'Çıxarış', 'İpoteka', 'Adres1', 'Adres2']
        
        # Initialize a list to store dictionaries of extracted data
        extracted_data = []

        # Iterate over each link
        for link in links:
            print(f"Processing link: {link}")
            try:
                # Request the content of the page
                response = requests.get(link)
                response.encoding = 'utf-8'
                html_content = response.text
                
                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Find all the div tags with the class 'title'
                titles = soup.find_all('div', class_='title')
                
                if not titles:
                    print(f"No titles found for link: {link}")
                    continue
                
                # Iterate over each title div
                for title in titles:
                    # Initialize a dictionary to store the extracted information for each title
                    title_data = {key: None for key in columns}
                    
                    # Extract the price
                    price_tag = title.find('price')
                    price = price_tag.get_text(strip=True) if price_tag else None
                    title_data['Qiymet'] = price
                    
                    # Extract information from each titem tag
                    titems = title.find_all('titem')
                    for titem in titems:
                        # Extract the text directly within the titem tag
                        key_text = titem.get_text(strip=True, separator=' ').split('<g>')[0].strip(':').split(' ')[0]
                        
                        # Extract the text within the b tag inside the g tag
                        g_tag = titem.find('g')
                        if g_tag:
                            b_tag = g_tag.find('b')
                            value_text = b_tag.get_text(strip=True) if b_tag else None
                        else:
                            value_text = None
                        

                        print('--------------')
                        print('Key: ',key_text)
                        print('Value: ',value_text)
                        print('----------------')

                        if ':' in key_text:
                            key_text = key_text.replace(':', '')
                            title_data[key_text] = value_text
                        else:
                            title_data[key_text] = value_text

                        
                    
                    # Find the first div with the class 'box'
                    box_div = soup.find('div', class_='box')
                    if box_div:
                        text_box = box_div.get_text(strip=True).split('/')[1].split(' ')[1]
                        title_data['Emlak'] = text_box

                        # Extract the text from the emlak tag inside the box div
                        emlak_tag = box_div.find('emlak')
                        emlak_text = emlak_tag.get_text(strip=True) if emlak_tag else None
                        title_data['Emlak'] = emlak_text
                        
                        # Extract information from each params div inside the box div
                        params_divs = box_div.find_all('div', class_='params')
                        param_keys = ['Otaq sayı', 'Sahə', 'Mərtəbə', 'Çıxarış', 'Adres1', 'Adres2']

                        i = 0
                        for params in params_divs:
                            title_data[param_keys[i]] = params.get_text(strip=True)
                            i += 1
                            if i == 6:
                                break
                        title_data["Kateqoriya"] = text_box

                    # Add the dictionary for the current title to the extracted_data list
                    extracted_data.append(title_data)
                    time.sleep(2)
            except Exception as e:
                print(f"An error occurred while processing link {link}: {e}")

        # Convert the list of dictionaries to a DataFrame and concatenate with the existing DataFrame
        new_data_df = pd.DataFrame(extracted_data, columns=columns)
        print(new_data_df.shape)
        print(new_data_df.head())
        
        return new_data_df
    except Exception as e:
        print(e)
        return None

def save_data(df, filepath):
    if df is not None:
        df.to_csv(filepath, index=False)
        print(f"Data saved to '{filepath}'")
    else:
        print("No data to save.")
