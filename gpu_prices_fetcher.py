import requests
import csv

# Set your Perplexity AI API key
API_KEY = 'API_KEY'

# Define the prompts to fetch data
prompts = {
    "NVIDIA RTX 4090 Price": "What is the current market price for the NVIDIA RTX 4090 GPU?",
    "NVIDIA RTX 6000 Ada Generation Price": "What is the latest price for the NVIDIA RTX 6000 Ada Generation GPU?",
    "NVIDIA A100 Tensor Core GPU Price": "How much does the NVIDIA A100 Tensor Core GPU cost currently?",
    "AMD Ryzen Threadripper PRO 5995WX Price": "What is the current price of the AMD Ryzen Threadripper PRO 5995WX CPU?",
    "Intel Xeon W-3375 Processor Price": "What is the latest price for the Intel Xeon W-3375 processor?",
    "High-end Motherboard Price": "What is the price of high-end motherboards that support multiple GPUs, such as the ASUS Pro WS WRX80E-SAGE SE WIFI?",
    "128GB DDR4 ECC RAM Price": "What is the current cost of 128GB DDR4 ECC RAM?",
    "2TB NVMe SSD Price": "How much does a 2TB NVMe SSD, like the Samsung 980 PRO, cost now?",
    "4TB Enterprise-grade HDD Price": "What is the price of a 4TB enterprise-grade HDD?",
    "Custom Liquid Cooling System Price": "What are the current prices for custom liquid cooling systems suitable for high-end GPU rigs?",
    "1600W Platinum-rated PSU Price": "How much does a 1600W Platinum-rated PSU, such as the Corsair AX1600i, cost currently?",
    "10 Gigabit Ethernet NIC Price": "What is the price of a 10 Gigabit Ethernet Network Interface Card today?",
    "10GbE Network Switch Price": "What is the current cost of a 10GbE network switch with at least 8 ports?",
    "Average Electricity Rate": "What is the average commercial electricity rate per kWh in [Your City/Region] as of [Current Month and Year]?",
    "Professional IT Services Rate": "What are the current rates for professional IT services specializing in setting up GPU clusters?"
}

# Function to fetch data from Perplexity AI API
def fetch_data(prompt):
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "top_p": 0.9,
        "search_recency_filter": "month",
        "frequency_penalty": 1,
        "stream": False
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()

    # Extract the assistant's reply
    assistant_message = result['choices'][0]['message']['content']
    return assistant_message.strip()

# Open a CSV file to write the data
with open('perplexity_hardware_prices.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Item', 'Information']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for item, prompt in prompts.items():
        print(f"Fetching data for: {item}")
        try:
            result = fetch_data(prompt)
            writer.writerow({'Item': item, 'Information': result})
        except Exception as e:
            print(f"An error occurred while fetching data for {item}: {e}")
            writer.writerow({'Item': item, 'Information': 'Error fetching data'})

print("Data has been written to 'perplexity_hardware_prices.csv'")