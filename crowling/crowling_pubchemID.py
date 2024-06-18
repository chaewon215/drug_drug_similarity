import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def drugbank_meta_crowling(drug, df):
    
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument("headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_option)
    
    # drugbank 홈페이지
    driver.get('https://go.drugbank.com/drugs/' + drug)

    err_list = []

    try:
        external_links = driver.find_element(By.ID, 'pubchem-compound')
        dd_element = external_links.find_element(By.XPATH, 'following-sibling::dd[1]')
        pubchem_id = dd_element.text
    
        df_add = pd.DataFrame({'#Drug': [drug], 'Pubchem CID': [pubchem_id]})
        # print(df_add)
        df = pd.concat([df, df_add], ignore_index=False)
                    
    except Exception as e:
        print("Error: ", e)
        err_list.append(drug)


    if len(err_list) != 0:
        print(f"Error: '{drug}' 정보 수집 실패")
    else:
        print(f"'{drug}'의 정보 수집 완료")
    driver.close()
    return df


if __name__ == '__main__':
    dti = pd.read_csv('ChG-Miner_miner-chem-gene.tsv', sep='\t')
    df = pd.DataFrame(columns=['#Drug', 'Pubchem CID'])


    for i in range(0, len(dti)):
        if dti['#Drug'][i] not in df['#Drug'].values:
            df = drugbank_meta_crowling(dti['#Drug'][i], df)

        if i % 10 == 0:
            df.to_csv('drug_id.csv', index=False)
            print(f"Save {i}th data")
            print("Complete percent: ", i/len(dti)*100)
