import requests
import os
from typing import Optional
from urllib.parse import quote_plus
import logging

class AcademicPaperFetcher:
    def __init__(self):
        self.base_urls = {
            'arxiv': 'https://arxiv.org/pdf/',
            'ieee': 'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber='
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def fetch_paper(self, identifier: str, source: str = 'arxiv', output_dir: str = './papers') -> Optional[str]:
        """Fetch paper PDF by identifier"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            url = self._build_url(identifier, source)
            
            response = requests.get(url, headers=self.headers, stream=True)
            response.raise_for_status()

            filename = os.path.join(output_dir, f"{identifier.replace('/', '_')}.pdf")
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.logger.info(f"Successfully downloaded: {filename}")
            return filename

        except Exception as e:
            self.logger.error(f"Error fetching paper: {e}")
            return None

    def _build_url(self, identifier: str, source: str) -> str:
        """Build URL based on source and identifier"""
        base_url = self.base_urls.get(source.lower())
        if not base_url:
            raise ValueError(f"Unsupported source: {source}")
        
        if source == 'arxiv':
            return f"{base_url}{identifier}"
        elif source == 'ieee':
            return f"{base_url}{identifier}"

def main():
    fetcher = AcademicPaperFetcher()
    # Example usage for arXiv paper
    paper_id = "2103.13415"  # Example arXiv ID
    fetcher.fetch_paper(paper_id, 'arxiv')

if __name__ == "__main__":
    main()