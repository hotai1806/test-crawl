import requests
from bs4 import BeautifulSoup
import json
# URL của trang cần cào
# url = 'https://diemthi.vnexpress.net/tra-cuu-dai-hoc/nhom-nganh/id/21'
url = "https://diemthi.vnexpress.net/diem-chuan/nganh/searchspecv2/1/spec_1/Th%E1%BB%A7y%20s%E1%BA%A3n%20-%20L%C3%A2m%20Nghi%E1%BB%87p%20-%20N%C3%B4ng%20nghi%E1%BB%87p/spec_2//spec_3//spec_4//spec_5//spid_1/21/block_name/all/sortby/1/college_type/2"
# Gửi yêu cầu GET đến trang web
response = requests.get(url)
# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.text
    json_html = response.json()
    # html_content = data['html']
    
    clean_content = data.replace('\t', '').strip()
    soup1 = BeautifulSoup(clean_content, 'html.parser').prettify()
    soup = BeautifulSoup(soup1,'html.parser' )

    # print(soup)

    # If you want to replace all tab characters, use:
    # Extract the rows from the table
    table = soup.find('table')
    # print(table)
    rows = table.find('tbody').find_all('tr')

    # Prepare to collect the extracted data
    data = []

    # Loop through each row to extract information
    for row in rows:
        cols = row.find_all('td')
        # print(cols)
        with open('nganh_hoc.txt', 'w', encoding='utf-8') as file:
        # Write headers
            file.write(str(cols)+ "\n")
        # Extract individual data points
        stt = cols[0].text.strip()
        ten_nganh = cols[0].find('a').text.strip()
        ma_nganh = cols[0].find('span').text.strip()
        diem_chuan = cols[2].text.strip()
        to_hop_mon = cols[3].text.strip()
        hoc_phi = cols[4].text.strip()
        truong = cols[5].find('a').text.strip()

        # Add the extracted row to the data list
        data.append({
            'STT': stt,
            'Tên ngành': ten_nganh,
            'Mã ngành': ma_nganh,
            'Điểm chuẩn': diem_chuan,
            'Tổ hợp môn': to_hop_mon,
            'Học phí': hoc_phi,
            'Tên trường': truong
        })

    # Output the data or save it to a file
    for entry in data:
        print(entry)
    
    # # Open a file to write the data
    # with open('nganh_hoc.txt', 'w', encoding='utf-8') as file:
    #     # Write headers
    #     file.write(f"{'Mã ngành':<15} {'Tên ngành':<50} {'Điểm chuẩn':<15} {'Khối':<10} {'Trường':<30}\n")
    #     file.write("="*120 + "\n")
    #     file.write(response.text)
    #     # Loop through the data and write each entry to the file
    #     for entry in data['data']:
    #         ma_nganh = entry.get('code', 'N/A')
    #         ten_nganh = entry.get('spec', 'N/A')
    #         diem_chuan = entry.get('benchmark', 'N/A')
    #         khoi = entry.get('block_name', 'N/A')
    #         truong = entry.get('university_name', 'N/A')
            
    #         # Write each row of data
    #         file.write(f"{ma_nganh:<15} {ten_nganh:<50} {diem_chuan:<15} {khoi:<10} {truong:<30}\n")
    
    print("Data successfully written to nganh_hoc.txt")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
# Kiểm tra phản hồi có thành công hay không
# if response.status_code == 200:
#     # Phân tích nội dung HTML của trang
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Tìm tất cả các hàng dữ liệu có chứa thông tin về điểm thi
#     rows = soup.find_all('tr', class_='university__benchmark')
#     print('1',rows)


#     # Duyệt qua từng hàng và lấy thông tin nếu Mã ngành là 7620301
#     for row in rows:
#         ma_nganh_span = row.find('span')
#         print('1')

#         if ma_nganh_span and ma_nganh_span.text.strip() == '7620301':
#             # Lấy thông tin của ngành đó
#             ten_nganh = row.find('a').text.strip()
#             diem_chuan = row.find_all('span')[1].text.strip()  # Assuming the second <span> contains the score
#             khoi = row.find_all('td')[3].text.strip()
#             truong = row.find('p', class_='university__benchmark-name').text.strip()

#             # In ra kết quả
#             print('1')
#             print(f"Mã ngành: 7620301, Tên ngành: {ten_nganh}, Điểm chuẩn: {diem_chuan}, Khối: {khoi}, Trường: {truong}")
#             break
# else:
#     print(f"Yêu cầu thất bại với mã lỗi {response.status_code}")